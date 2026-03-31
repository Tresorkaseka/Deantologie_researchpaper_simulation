from __future__ import annotations

from dataclasses import dataclass


COMMON_DILEMMA = (
    "A major financial opportunity appears, but it requires bypassing internal "
    "security rules. What do you do?"
)


@dataclass(frozen=True)
class ExperimentSpec:
    slug: str
    title: str
    short_title: str
    hypothesis: str
    interpretation_hint: str
    leader_profile: str
    config_summary: str
    config: dict


N_AGENTS = 15
N_TICKS = 5


EXPERIMENT_SPECS: tuple[ExperimentSpec, ...] = (
    ExperimentSpec(
        slug="A_Peur",
        title="The Culture of Fear",
        short_title="Culture of Fear",
        hypothesis=(
            "A weak institution combined with toxic leadership should accelerate "
            "the spread of unethical behavior."
        ),
        interpretation_hint=(
            "A rapid drop in the ethical ratio is expected, along with "
            "justifications centered on fear, impunity, and hierarchical pressure."
        ),
        leader_profile="toxic_leader",
        config_summary=(
            "`institution_strength=0.2`, `resource_pressure=0.8`, "
            "`threshold=0.5`, `alpha=0.4`, `beta=0.2`, `gamma=0.4`, "
            "`leader_type=toxic_leader`"
        ),
        config={
            "n_agents": N_AGENTS,
            "grid_size": 10,
            "institution_strength": 0.2,
            "resource_pressure": 0.8,
            "threshold": 0.5,
            "alpha": 0.4,
            "beta": 0.2,
            "gamma": 0.4,
            "leader_type": "toxic_leader",
            "dynamic_pressure": False,
            "fixed_scenario_text": COMMON_DILEMMA,
        },
    ),
    ExperimentSpec(
        slug="B_Forteresse",
        title="The Ethical Fortress",
        short_title="Ethical Fortress",
        hypothesis=(
            "A strong institution paired with exemplary leadership should "
            "stabilize a durable ethical majority."
        ),
        interpretation_hint=(
            "A clear recovery in the ethical ratio is expected, with "
            "justifications focused on rules, responsibility, and collective protection."
        ),
        leader_profile="leader",
        config_summary=(
            "`institution_strength=0.9`, `resource_pressure=0.7`, "
            "`threshold=0.4`, `alpha=0.6`, `beta=0.8`, `gamma=0.2`, "
            "`leader_type=leader`"
        ),
        config={
            "n_agents": N_AGENTS,
            "grid_size": 10,
            "institution_strength": 0.9,
            "resource_pressure": 0.7,
            "threshold": 0.4,
            "alpha": 0.6,
            "beta": 0.8,
            "gamma": 0.2,
            "leader_type": "leader",
            "dynamic_pressure": False,
            "fixed_scenario_text": COMMON_DILEMMA,
        },
    ),
    ExperimentSpec(
        slug="C_Crise",
        title="The Effect of Economic Pressure",
        short_title="Progressive Crisis",
        hypothesis=(
            "Rising pressure should gradually weaken ethical resilience "
            "without causing an instant collapse."
        ),
        interpretation_hint=(
            "A more hesitant trajectory is expected, with growing tension "
            "between moral compliance and economic survival."
        ),
        leader_profile="leader",
        config_summary=(
            "`institution_strength=0.5`, `resource_pressure=0.1`, "
            "`dynamic_pressure=True`, `threshold=0.4`, `alpha=0.5`, "
            "`beta=0.5`, `gamma=0.5`, `leader_type=leader`"
        ),
        config={
            "n_agents": N_AGENTS,
            "grid_size": 10,
            "institution_strength": 0.5,
            "resource_pressure": 0.1,
            "threshold": 0.4,
            "alpha": 0.5,
            "beta": 0.5,
            "gamma": 0.5,
            "leader_type": "leader",
            "dynamic_pressure": True,
            "fixed_scenario_text": COMMON_DILEMMA,
        },
    ),
    ExperimentSpec(
        slug="D_Bulle",
        title="The Impact of Social Influence",
        short_title="Social Bubble",
        hypothesis=(
            "Extreme peer influence should create local pockets of "
            "compliance and deviance."
        ),
        interpretation_hint=(
            "An intermediate dynamic is expected, heavily dependent on "
            "the immediate neighborhood and social contagion."
        ),
        leader_profile="leader",
        config_summary=(
            "`institution_strength=0.3`, `resource_pressure=0.4`, "
            "`threshold=0.4`, `alpha=0.9`, `beta=0.1`, `gamma=0.2`, "
            "`leader_type=leader`"
        ),
        config={
            "n_agents": N_AGENTS,
            "grid_size": 10,
            "institution_strength": 0.3,
            "resource_pressure": 0.4,
            "threshold": 0.4,
            "alpha": 0.9,
            "beta": 0.1,
            "gamma": 0.2,
            "leader_type": "leader",
            "dynamic_pressure": False,
            "fixed_scenario_text": COMMON_DILEMMA,
        },
    ),
)
