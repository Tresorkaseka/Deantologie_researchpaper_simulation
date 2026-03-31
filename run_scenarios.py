import sys

sys.stdout.reconfigure(encoding="utf-8")

import os

import matplotlib.pyplot as plt
from dotenv import load_dotenv

from llm_backend import get_llm_api_key, get_llm_base_url, get_llm_model_name, get_llm_provider
from model import EthicalOrgModel
from scenarios import SCENARIOS


load_dotenv()

CONFIG = {
    "n_agents": 40,
    "grid_size": 10,
    "institution_strength": 0.5,
    "resource_pressure": 0.3,
    "threshold": 0.4,
    "alpha": 0.4,
    "beta": 0.4,
    "gamma": 0.2,
    "model_name": get_llm_model_name(),
    "llm_api_key": get_llm_api_key(),
    "llm_provider": get_llm_provider(),
    "llm_base_url": get_llm_base_url(),
}

N_TICKS = 8
results = {}


if __name__ == "__main__":
    print("\n--- COMPARATIVE SCENARIO SIMULATION (Research paper) ---")
    print(f"Agents: {CONFIG['n_agents']} | Ticks: {N_TICKS}")
    print(f"Model: {CONFIG['model_name']}\n")

    for scenario in SCENARIOS:
        scenario_id = scenario["id"]
        print("============================================================")
        print(f">> SCENARIO: {scenario_id}")
        print("============================================================")

        CONFIG["fixed_scenario_text"] = scenario["text"]
        model = EthicalOrgModel(**CONFIG)

        for tick in range(N_TICKS):
            model.step()
            print(f"  {scenario_id} - Tick {tick + 1}/{N_TICKS} completed.")

        results[scenario_id] = model.summary()

    os.makedirs("results", exist_ok=True)
    plt.close("all")
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = {
        "PROFIT_VS_SAFETY": "#e74c3c",
        "DATA_PRIVACY": "#9b59b6",
        "WHISTLEBLOWING": "#3498db",
        "FAIR_COMPETITION": "#f1c40f",
    }

    for scenario_id, df in results.items():
        color = colors.get(scenario_id, "#333333")
        ax.plot(
            df.index,
            df["EthicalRatio"],
            label=scenario_id,
            color=color,
            linewidth=2.5,
            marker="o",
        )

    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.8, label="Survival threshold (50%)")
    ax.set_title(
        "Comparative ethical resilience by scenario\n(Evolution of the global ethical ratio)",
        fontsize=13,
        fontweight="bold",
    )
    ax.set_xlabel("Time (ticks)")
    ax.set_ylabel("Ethical ratio (0 to 1)")
    ax.set_ylim(0, 1.05)
    ax.legend(title="Tested dilemmas", bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    output_path = "results/conclusion_comparative_papier.png"
    plt.savefig(output_path, dpi=200, bbox_inches="tight")

    print("\nComparative simulation completed.")
    print(f"Summary chart generated: {output_path}")
