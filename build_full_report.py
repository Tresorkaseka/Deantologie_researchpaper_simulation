from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from research_config import EXPERIMENT_SPECS


ROOT = Path(__file__).resolve().parent
DOCS_DIR = ROOT / "docs"
RESULTS_DIR = ROOT / "results"
SCENARIOS_DIR = RESULTS_DIR / "scenarios"
SUMMARY_PATH = RESULTS_DIR / "scenario_summary.csv"


@dataclass
class ScenarioBundle:
    slug: str
    title: str
    short_title: str
    hypothesis: str
    config_summary: str
    interpretation: str
    metrics: pd.DataFrame
    log_text: str


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    headers = ["Observation"] + list(df.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for observation, row in df.iterrows():
        values = [str(observation)] + [
            f"{value:.3f}" if isinstance(value, float) else str(value)
            for value in row.tolist()
        ]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def load_scenario_bundle(spec) -> ScenarioBundle:
    scenario_dir = SCENARIOS_DIR / spec.slug
    metrics = pd.read_csv(scenario_dir / "metrics.csv", index_col="observation")
    interpretation = (scenario_dir / "interpretation.txt").read_text(encoding="utf-8").strip()
    log_text = (scenario_dir / "conversation_log.txt").read_text(encoding="utf-8").strip()

    return ScenarioBundle(
        slug=spec.slug,
        title=spec.title,
        short_title=spec.short_title,
        hypothesis=spec.hypothesis,
        config_summary=spec.config_summary,
        interpretation=interpretation,
        metrics=metrics,
        log_text=log_text,
    )


def build_summary_table(summary_df: pd.DataFrame) -> str:
    lines = [
        "| Scenario | Initial ratio | Final ratio | Peak observed | Final unethical agents |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in summary_df.itertuples(index=False):
        lines.append(
            f"| {row.short_title} | {row.initial_ratio:.3f} | {row.final_ratio:.3f} | "
            f"{row.peak_ratio:.3f} | {row.final_nonethical} |"
        )
    return "\n".join(lines)


def load_summary() -> pd.DataFrame:
    if not SUMMARY_PATH.exists():
        raise FileNotFoundError(
            "The file results/scenario_summary.csv was not found. "
            "Run python run_research_experiments.py first."
        )
    return pd.read_csv(SUMMARY_PATH)


def build_main_report(summary_df: pd.DataFrame, bundles: list[ScenarioBundle]) -> str:
    lines = [
        "# Organizational ethics simulation",
        "",
        "## Abstract",
        (
            "This project simulates the evolution of an ethics culture inside a "
            "technology organization by combining agent-based modeling with "
            "LLM-generated justifications. Four structural scenarios were rerun: "
            "the culture of fear, the ethical fortress, the progressive crisis, "
            "and the social bubble. The results show that institutional strength "
            "is the most protective factor, while managerial fear and economic "
            "pressure significantly weaken the collective norm."
        ),
        "",
        "**Keywords**: agent-based modeling, ethics, organizational culture, LLM explanation, ethical simulation",
        "",
        "## 1. Scientific objective",
        (
            "The goal is to study how a professional collective arbitrates between "
            "compliance, opportunism, and contextual pressure. The model does not "
            "only try to predict a final state; it also tries to make visible the "
            "rationalizations agents use when they accept or reject a transgression."
        ),
        "",
        "## 2. How the model works",
        "- Each agent occupies a position on a grid and interacts with a local neighborhood.",
        "- A behavioral score combines peer influence, institutional strength, and economic pressure.",
        "- An LLM produces a short textual justification that validates or nuances the behavioral transition.",
        "- Ethical or toxic leaders act as stable poles of influence in the ecosystem.",
        "",
        "## 3. LLM contribution",
        (
            "The main contribution of the LLM is explanatory. In a classic simulation, "
            "an agent changes state because a numeric threshold is crossed. Here, the "
            "LLM adds an interpretive layer: it states the motive invoked by the agent, "
            "for example loyalty to the institution, fear of retaliation, alignment "
            "with colleagues, or the search for gain. This qualitative layer transforms "
            "a purely statistical output into material that is closer to an "
            "organizational study."
        ),
        "",
        "## 4. Experimental protocol",
        build_summary_table(summary_df),
        "",
        "![Cross-scenario comparison of the ethical ratio](../results/graph_papier_recherche.png)",
        "",
        "## 5. Detailed results",
        "",
    ]

    for bundle in bundles:
        lines.extend(
            [
                f"### {bundle.title}",
                f"**Hypothesis**: {bundle.hypothesis}",
                f"**Configuration**: {bundle.config_summary}",
                f"**Interpretation**: {bundle.interpretation}",
                "",
                f"![Quantitative results - {bundle.short_title}](../results/scenarios/{bundle.slug}/metrics.png)",
                "",
                f"![Conversation excerpt - {bundle.short_title}](../results/scenarios/{bundle.slug}/conversation_snapshot.png)",
                "",
                f"![Initial grid - {bundle.short_title}](../results/scenarios/{bundle.slug}/grid_initial.png)",
                "",
                f"![Final grid - {bundle.short_title}](../results/scenarios/{bundle.slug}/grid_final.png)",
                "",
            ]
        )

    lines.extend(
        [
            "## 6. Overall discussion",
            (
                "The comparison highlights three dynamics. First, the ethical fortress "
                "shows that a strong institution reduces moral ambiguity and supports "
                "hesitant agents. Second, the culture of fear captures the corrosive "
                "effect of a toxic leader: rationalizations become defensive, utilitarian, "
                "and centered on impunity. Third, the crisis and social bubble scenarios "
                "suggest that deviations do not arise only from individual convictions, "
                "but also from local arrangements and a context of scarcity."
            ),
            "",
            "## 7. Conclusion",
            (
                'The project shows that an LLM can enrich a multi-agent model by making '
                'the "why" of transitions observable. This hybridization does not replace '
                "quantitative analysis; it makes it interpretable. For a research paper, "
                "the value of the system lies in the articulation between metrics, spatial "
                "visualizations, and conversational traces."
            ),
        ]
    )

    return "\n".join(lines).strip() + "\n"


def build_appendix_report(summary_df: pd.DataFrame, bundles: list[ScenarioBundle]) -> str:
    lines = [
        "# Appendices - Logs and detailed tables",
        "",
        "## 1. Overview",
        build_summary_table(summary_df),
        "",
        "## 2. Scenario logs",
        "",
    ]

    for bundle in bundles:
        lines.extend(
            [
                "<div class='page-break'></div>",
                f"## {bundle.title}",
                f"**Configuration**: {bundle.config_summary}",
                f"**Synthetic interpretation**: {bundle.interpretation}",
                "",
                "### Full table",
                dataframe_to_markdown(bundle.metrics),
                "",
                "### Conversation log",
                "```text",
                bundle.log_text,
                "```",
                "",
            ]
        )

    return "\n".join(lines).strip() + "\n"


def build_project_doc(summary_df: pd.DataFrame, bundles: list[ScenarioBundle]) -> str:
    lines = [
        "# Project documentation",
        "",
        "## 1. What the project does",
        (
            "The project simulates a technology organization in which professionals "
            "must arbitrate between following rules and taking opportunities to "
            "transgress them. The goal is not only to count behavioral shifts, but "
            "to understand the reasoning invoked to justify them."
        ),
        "",
        "## 2. Architecture",
        "- `model.py` defines the Mesa environment, the population, and the global metrics.",
        "- `agents.py` defines agent profiles and the LLM call.",
        "- `research_config.py` centralizes the structural research scenarios.",
        "- `run_research_experiments.py` reruns the experiments and produces visual artifacts.",
        "- `build_full_report.py` transforms the results into usable documents.",
        "- `docs/generate_pdf.py` exports the public documentation package to PDF with Mermaid rendering.",
        "",
        "## 3. Agent decision cycle",
        "1. The agent observes its neighborhood and computes a local score.",
        "2. The system builds a contextual prompt.",
        "3. The LLM formulates a short, justified decision.",
        "4. The model updates the agent type according to the score and the answer.",
        "5. The results are collected for charts and reports.",
        "",
        "## 4. Why use an LLM here?",
        (
            "The LLM is not used to replace the model logic, but to explain the "
            "agent's situated logic. It makes it possible to visualize motives such "
            "as hierarchical loyalty, fear, social alignment, or profit seeking. "
            "That makes the results closer to a qualitative field analysis."
        ),
        "",
        "## 5. Artifacts produced after a rerun",
        "- One global table: `results/scenario_summary.csv`.",
        "- One `results/scenarios/<slug>/` folder for each scenario.",
        "- One comparative curve: `results/graph_papier_recherche.png`.",
        "- One main report, appendices, ODD documentation, and a maintenance guide.",
        "",
        "## 6. Quick reading of the current results",
        build_summary_table(summary_df),
        "",
    ]

    for bundle in bundles:
        lines.extend(
            [
                f"### {bundle.title}",
                bundle.interpretation,
                "",
            ]
        )

    return "\n".join(lines).strip() + "\n"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    summary_df = load_summary()
    bundles = [load_scenario_bundle(spec) for spec in EXPERIMENT_SPECS]

    write_text(DOCS_DIR / "Rapport_Recherche_Simulations.md", build_main_report(summary_df, bundles))
    write_text(DOCS_DIR / "Rapport_Complet_Simulations.md", build_appendix_report(summary_df, bundles))
    write_text(DOCS_DIR / "Documentation_Projet.md", build_project_doc(summary_df, bundles))
    print("Markdown documents regenerated from the latest scenario outputs.")


if __name__ == "__main__":
    main()
