from __future__ import annotations

import random
from collections import Counter

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from agents import ProfessionalAgent
from llm_backend import DEFAULT_MODEL_NAME


def count_type(model: "EthicalOrgModel", agent_type: str) -> int:
    return sum(
        1
        for agent in model.schedule.agents
        if isinstance(agent, ProfessionalAgent) and agent.agent_type == agent_type
    )


def compute_total_agents(model: "EthicalOrgModel") -> int:
    return sum(
        1 for agent in model.schedule.agents if isinstance(agent, ProfessionalAgent)
    )


def build_agent_types(total_agents: int, leader_type: str) -> list[str]:
    shares = [
        ("ethical", 0.35),
        ("non_ethical", 0.30),
        ("neutral", 0.25),
        (leader_type, 0.10),
    ]

    counts = {name: int(total_agents * share) for name, share in shares}
    assigned = sum(counts.values())
    remainders = sorted(
        ((name, (total_agents * share) - counts[name]) for name, share in shares),
        key=lambda item: item[1],
        reverse=True,
    )

    for name, _ in remainders:
        if assigned >= total_agents:
            break
        counts[name] += 1
        assigned += 1

    population: list[str] = []
    for name, _ in shares:
        population.extend([name] * counts[name])
    random.shuffle(population)
    return population


class EthicalOrgModel(Model):
    """
    ODD simulation of ethical dynamics inside a tech organization.

    Data collection records an initial state and one state after each tick,
    which makes the curves directly interpretable in the reports.
    """

    def __init__(
        self,
        n_agents=60,
        grid_size=10,
        peer_influence=0.6,
        institution_strength=0.5,
        resource_pressure=0.3,
        threshold=0.4,
        model_name=None,
        llm_api_key=None,
        llm_provider="custom",
        llm_base_url=None,
        alpha=0.4,
        beta=0.4,
        gamma=0.2,
        **kwargs,
    ):
        super().__init__()
        self.n_agents = n_agents
        self.peer_influence = peer_influence
        self.institution_strength = institution_strength
        self.resource_pressure = resource_pressure
        self.threshold = threshold
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.current_tick = 0

        self.model_name = model_name or kwargs.get("llm_model_name") or DEFAULT_MODEL_NAME
        self.llm_api_key = llm_api_key or kwargs.get("llm_api_key")
        self.llm_provider = llm_provider
        self.llm_base_url = llm_base_url or kwargs.get("llm_base_url")
        self.fixed_scenario_text = kwargs.get("fixed_scenario_text")
        self.dynamic_pressure = kwargs.get("dynamic_pressure", False)
        self.leader_type = kwargs.get("leader_type", "leader")

        self.grid = MultiGrid(grid_size, grid_size, torus=True)
        self.schedule = RandomActivation(self)

        for agent_id, agent_type in enumerate(
            build_agent_types(self.n_agents, self.leader_type)
        ):
            agent = ProfessionalAgent(agent_id, self, agent_type)
            x = random.randrange(grid_size)
            y = random.randrange(grid_size)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

        self.datacollector = DataCollector(
            model_reporters={
                "Ethical": lambda model: count_type(model, "ethical"),
                "NonEthical": lambda model: count_type(model, "non_ethical"),
                "Neutral": lambda model: count_type(model, "neutral"),
                "Leader": lambda model: count_type(model, "leader")
                + count_type(model, "toxic_leader"),
                "TotalAgents": compute_total_agents,
                "EthicalRatio": lambda model: (
                    (
                        count_type(model, "ethical")
                        + count_type(model, "leader")
                        + count_type(model, "toxic_leader")
                    )
                    / max(1, compute_total_agents(model))
                ),
            }
        )
        self.datacollector.collect(self)

    def _print_state_snapshot(self) -> None:
        snapshot = Counter(
            agent.agent_type
            for agent in self.schedule.agents
            if isinstance(agent, ProfessionalAgent)
        )
        print(f"\n{'=' * 60}")
        print(f"  TICK {self.current_tick}")
        print(
            "  Ethical={ethical} | NonEthical={nonethical} | Neutral={neutral} | "
            "Leader={leader} | ToxicLeader={toxic} | Total={total}".format(
                ethical=snapshot.get("ethical", 0),
                nonethical=snapshot.get("non_ethical", 0),
                neutral=snapshot.get("neutral", 0),
                leader=snapshot.get("leader", 0),
                toxic=snapshot.get("toxic_leader", 0),
                total=sum(snapshot.values()),
            )
        )
        print(f"{'=' * 60}")

    def step(self):
        self.current_tick += 1
        self._print_state_snapshot()
        self.schedule.step()

        if self.dynamic_pressure:
            self.resource_pressure = min(1.0, self.resource_pressure + 0.01)

        self.datacollector.collect(self)

    def summary(self):
        df = self.datacollector.get_model_vars_dataframe()
        print("\n" + "=" * 60)
        print("  SIMULATION SUMMARY")
        print("=" * 60)
        print(df.to_string())
        return df
