from __future__ import annotations

import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from llm_backend import (
    get_llm_api_key,
    get_llm_base_url,
    get_llm_model_name,
    get_llm_provider,
)
from model import EthicalOrgModel
from research_config import EXPERIMENT_SPECS, N_TICKS
from viz import (
    draw_grid,
    plot_comparative_metrics,
    plot_scenario_metrics,
    render_conversation_snapshot,
)


sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
SCENARIOS_DIR = RESULTS_DIR / "scenarios"
RESULTS_DIR.mkdir(exist_ok=True)
SCENARIOS_DIR.mkdir(exist_ok=True)

load_dotenv(ROOT / ".env")

LLM_MODEL_NAME = get_llm_model_name()
LLM_API_KEY = get_llm_api_key()
LLM_PROVIDER = get_llm_provider()
LLM_BASE_URL = get_llm_base_url()


def build_interpretation(df: pd.DataFrame, hint: str) -> str:
    initial_ratio = float(df["EthicalRatio"].iloc[0])
    final_ratio = float(df["EthicalRatio"].iloc[-1])
    peak_ratio = float(df["EthicalRatio"].max())
    final_nonethical = int(df["NonEthical"].iloc[-1])
    delta = final_ratio - initial_ratio

    if delta >= 0.2:
        trend = "The trajectory shows a strong improvement in ethical robustness."
    elif delta >= 0.05:
        trend = "The trajectory indicates a moderate improvement in ethical robustness."
    elif delta <= -0.2:
        trend = "The trajectory reveals a sharp collapse in ethical robustness."
    elif delta <= -0.05:
        trend = "The trajectory reveals a gradual deterioration in ethical robustness."
    else:
        trend = "The trajectory remains broadly stable but exposes a fragile balance."

    return (
        f"{trend} {hint} The ethical ratio moves from {initial_ratio:.3f} to "
        f"{final_ratio:.3f}, with a peak at {peak_ratio:.3f}. "
        f"The last archived state contains {final_nonethical} unethical agents."
    )


def extract_snapshot_lines(log_text: str) -> list[str]:
    lines = []
    for raw_line in log_text.splitlines():
        stripped = raw_line.strip()
        if "[Agent" in stripped or stripped.startswith("TICK ") or "Ethical=" in stripped:
            lines.append(stripped)
        if len(lines) >= 18:
            break
    return lines


def run_experiment(spec) -> dict:
    scenario_dir = SCENARIOS_DIR / spec.slug
    scenario_dir.mkdir(parents=True, exist_ok=True)

    config = dict(spec.config)
    config["model_name"] = LLM_MODEL_NAME
    config["llm_api_key"] = LLM_API_KEY
    config["llm_provider"] = LLM_PROVIDER
    config["llm_base_url"] = LLM_BASE_URL

    model = EthicalOrgModel(**config)
    draw_grid(
        model,
        tick=0,
        output_path=scenario_dir / "grid_initial.png",
        title=f"{spec.title} - Initial grid",
    )

    log_buffer = io.StringIO()
    with redirect_stdout(log_buffer):
        print("#" * 70)
        print(f"SCENARIO: {spec.title}")
        print("#" * 70)
        for _ in range(N_TICKS):
            model.step()
        df = model.summary()

    draw_grid(
        model,
        tick=len(df) - 1,
        output_path=scenario_dir / "grid_final.png",
        title=f"{spec.title} - Final grid",
    )

    df.to_csv(scenario_dir / "metrics.csv", index_label="observation")
    plot_scenario_metrics(df, spec.title, scenario_dir / "metrics.png")

    log_text = log_buffer.getvalue()
    (scenario_dir / "conversation_log.txt").write_text(log_text, encoding="utf-8")

    snapshot_lines = extract_snapshot_lines(log_text)
    render_conversation_snapshot(
        title=f"{spec.title} - Conversation excerpt",
        subtitle="Agent decisions observed during the simulation",
        lines=snapshot_lines,
        output_path=scenario_dir / "conversation_snapshot.png",
    )

    interpretation = build_interpretation(df, spec.interpretation_hint)
    (scenario_dir / "interpretation.txt").write_text(interpretation, encoding="utf-8")

    return {
        "slug": spec.slug,
        "title": spec.title,
        "short_title": spec.short_title,
        "hypothesis": spec.hypothesis,
        "config_summary": spec.config_summary,
        "initial_ratio": float(df["EthicalRatio"].iloc[0]),
        "final_ratio": float(df["EthicalRatio"].iloc[-1]),
        "peak_ratio": float(df["EthicalRatio"].max()),
        "min_ratio": float(df["EthicalRatio"].min()),
        "final_ethical": int(df["Ethical"].iloc[-1]),
        "final_nonethical": int(df["NonEthical"].iloc[-1]),
        "final_neutral": int(df["Neutral"].iloc[-1]),
        "leader_count": int(df["Leader"].iloc[-1]),
        "interpretation": interpretation,
    }


def main() -> None:
    if not LLM_API_KEY:
        raise RuntimeError("LLM_API_KEY was not found in .env")

    print("\n" + "=" * 68)
    print("  RESEARCH SCENARIO RERUN")
    print("=" * 68 + "\n")

    summary_rows = []
    frames: dict[str, pd.DataFrame] = {}
    titles: dict[str, str] = {}

    for spec in EXPERIMENT_SPECS:
        print(f"-> Running: {spec.title}")
        summary = run_experiment(spec)
        summary_rows.append(summary)
        frames[spec.slug] = pd.read_csv(
            SCENARIOS_DIR / spec.slug / "metrics.csv",
            index_col="observation",
        )
        titles[spec.slug] = spec.short_title
        print(f"   done | final ratio = {summary['final_ratio']:.3f}")

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(RESULTS_DIR / "scenario_summary.csv", index=False)
    plot_comparative_metrics(frames, titles, RESULTS_DIR / "graph_papier_recherche.png")

    consolidated_log = []
    for spec in EXPERIMENT_SPECS:
        consolidated_log.append(f"SCENARIO RUN: {spec.title}")
        consolidated_log.append(
            (SCENARIOS_DIR / spec.slug / "conversation_log.txt")
            .read_text(encoding="utf-8")
            .strip()
        )
        consolidated_log.append("")
    (RESULTS_DIR / "rapport_brut_conversations.txt").write_text(
        "\n".join(consolidated_log).strip() + "\n",
        encoding="utf-8",
    )

    print("\nArtifacts created in results/scenarios/")
    print("Global summary: results/scenario_summary.csv")
    print("Comparative chart: results/graph_papier_recherche.png")


if __name__ == "__main__":
    main()
