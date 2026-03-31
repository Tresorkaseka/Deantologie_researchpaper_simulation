import sys

sys.stdout.reconfigure(encoding="utf-8")

import random
import time

from llm_backend import create_llm_client
from scenarios import SCENARIOS


SYSTEM_PROMPTS = {
    "ethical": (
        "You are an ethical professional in a tech company. "
        "You follow the rules, protect your colleagues, and reject corrupt practices. "
        "When you decide, you put fairness and institutional values first."
    ),
    "non_ethical": (
        "You are an opportunistic professional in a tech company. "
        "You prioritize personal gain. You may bypass rules, manipulate colleagues, "
        "and ignore directives if it benefits you."
    ),
    "neutral": (
        "You are an undecided professional in a tech company. "
        "You observe the people around you and tend to follow the dominant behavior "
        "in your immediate environment."
    ),
    "leader": (
        "You are a senior leader in a tech company. "
        "Your decisions set the tone for the whole team. You have strong ethical "
        "convictions and actively promote a culture of integrity and transparency. "
        "You exert strong influence over nearby agents."
    ),
    "toxic_leader": (
        "You are a cynical and toxic leader in a tech company. "
        "Your only priority is immediate profit and power. "
        "You impose a culture of silence, encourage dubious practices, and ignore "
        "ethics whenever it serves financial interests or your own."
    ),
}

TYPE_COLORS = {
    "ethical": "#2ecc71",
    "non_ethical": "#e74c3c",
    "neutral": "#f39c12",
    "leader": "#3498db",
    "toxic_leader": "#8e44ad",
}


def normalize_decision_text(text: str) -> str:
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
    }
    cleaned = " ".join(text.split())
    for source, target in replacements.items():
        cleaned = cleaned.replace(source, target)
    return cleaned


class ProfessionalAgent:
    def __init__(self, unique_id, model, agent_type: str):
        self.unique_id = unique_id
        self.model = model
        self.agent_type = agent_type
        self.pos = None
        self.influence_level = (
            0.85 if agent_type in ("leader", "toxic_leader") else random.uniform(0.2, 0.6)
        )
        self.social_sensitivity = (
            0.85 if agent_type == "neutral" else random.uniform(0.1, 0.5)
        )
        self.score_history = []
        self.decision_history = []

    def compute_score(self, neighbors):
        if not neighbors:
            return 0.0

        total_influence = sum(neighbor.influence_level for neighbor in neighbors)
        if total_influence == 0:
            peer_signal = 0.0
        else:
            ethical_influence = sum(
                neighbor.influence_level
                for neighbor in neighbors
                if neighbor.agent_type in ("ethical", "leader")
            )
            peer_signal = ethical_influence / total_influence

        institution = self.model.institution_strength
        pressure = self.model.resource_pressure

        score = (
            (self.social_sensitivity * self.model.alpha * peer_signal)
            + (self.model.beta * institution)
            - (self.model.gamma * pressure)
        )
        return round(score, 4)

    def ask_llm(self, situation: str) -> str:
        """Query the configured LLM backend with the agent's local context."""

        if not hasattr(self, "_llm_client"):
            self._llm_client = create_llm_client(
                api_key=self.model.llm_api_key,
                provider=self.model.llm_provider,
                base_url=self.model.llm_base_url,
            )

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self._llm_client.chat.completions.create(
                    model=self.model.model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPTS[self.agent_type],
                        },
                        {
                            "role": "user",
                            "content": (
                                f"Situation: {situation}\n\n"
                                "Respond in ONE short sentence of at most 22 words. "
                                "Start with ETHICAL or UNETHICAL, then explain why."
                            ),
                        },
                    ],
                    max_tokens=150,
                    temperature=0.7,
                )
                return response.choices[0].message.content.strip()
            except Exception as exc:
                error_text = str(exc)
                lowered = error_text.lower()
                is_transient = (
                    "429" in error_text
                    or "503" in error_text
                    or "rate_limit" in lowered
                    or "unavailable" in lowered
                    or "temporarily" in lowered
                )
                if is_transient:
                    wait = 5 * (2 ** attempt)
                    print(
                        f"    [Transient LLM error] Attempt {attempt + 1}/{max_retries}, waiting {wait}s..."
                    )
                    time.sleep(wait)
                else:
                    first_line = error_text.splitlines()[0].strip()
                    return f"[LLM error: {first_line}]"
        return "[LLM error: temporary service issue after 3 attempts]"

    def move(self):
        neighbors = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False,
        )
        self.model.grid.move_agent(self, random.choice(neighbors))

    def update_type(self, score: float, llm_decision: str):
        if self.agent_type in ("leader", "toxic_leader"):
            return

        normalized = llm_decision.lower().replace("_", " ").replace("-", " ")
        is_ethical = (
            "ethical" in normalized
            and "unethical" not in normalized
            and "not ethical" not in normalized
            and "non ethical" not in normalized
        )
        is_unethical = (
            "unethical" in normalized
            or "not ethical" in normalized
            or "non ethical" in normalized
        )

        effective_score = score + random.gauss(0, 0.03)

        if effective_score > self.model.threshold and is_ethical:
            self.agent_type = "ethical"
        elif effective_score < self.model.threshold and is_unethical:
            self.agent_type = "non_ethical"
        elif self.agent_type == "neutral":
            neighbors = self._get_neighbors()
            if neighbors:
                agent_types = [
                    neighbor.agent_type
                    for neighbor in neighbors
                    if neighbor.agent_type not in ("leader", "toxic_leader")
                ]
                if agent_types:
                    self.agent_type = max(set(agent_types), key=agent_types.count)

    def step(self):
        self.move()
        neighbors = self._get_neighbors()
        score = self.compute_score(neighbors)
        self.score_history.append(score)

        if getattr(self.model, "fixed_scenario_text", None):
            dilemma = self.model.fixed_scenario_text
        else:
            dilemma = random.choice(SCENARIOS)["text"]

        neighbor_summary = ", ".join(neighbor.agent_type for neighbor in neighbors[:4]) or "none"
        situation = (
            f"Tick {self.model.current_tick} | "
            f"Dilemma: {dilemma} | "
            f"Nearby colleagues: {neighbor_summary}. "
            f"Resource pressure: {self.model.resource_pressure:.1f}, "
            f"Institutional strength: {self.model.institution_strength:.1f}. "
            f"Your ethical score: {score:.2f} (threshold={self.model.threshold:.2f})."
        )
        decision = normalize_decision_text(self.ask_llm(situation))
        self.decision_history.append(decision)
        print(f"  [Agent {self.unique_id:03d} | {self.agent_type:12s}] {decision}")
        self.update_type(score, decision)

    def _get_neighbors(self):
        radius = 3 if self.agent_type in ("leader", "toxic_leader") else 2
        neighborhood = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False,
            radius=radius,
        )
        return [
            agent
            for cell in neighborhood
            for agent in self.model.grid.get_cell_list_contents([cell])
            if isinstance(agent, ProfessionalAgent) and agent.unique_id != self.unique_id
        ]
