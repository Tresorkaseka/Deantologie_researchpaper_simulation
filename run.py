import sys

sys.stdout.reconfigure(encoding="utf-8")

import matplotlib.pyplot as plt
from dotenv import load_dotenv

from llm_backend import get_llm_api_key, get_llm_base_url, get_llm_model_name, get_llm_provider
from model import EthicalOrgModel
from viz import draw_grid, plot_results


load_dotenv()

CONFIG = {
    "n_agents": 60,
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

N_TICKS = 10


if __name__ == "__main__":
    print("\nStarting the ODD simulation...")
    print(
        f"   Agents: {CONFIG['n_agents']} | Grid: {CONFIG['grid_size']}x{CONFIG['grid_size']} | "
        f"Ticks: {N_TICKS}"
    )
    print(f"   LLM model: {CONFIG['model_name']}")
    print(f"   LLM API: {'Configured' if CONFIG['llm_api_key'] else 'Not configured'}\n")

    model = EthicalOrgModel(**CONFIG)

    draw_grid(model, tick=0)
    plt.pause(2)
    plt.close("all")

    for tick in range(N_TICKS):
        model.step()
        plt.close("all")
        draw_grid(model, tick=tick + 1)
        plt.pause(2)

    df = model.summary()
    plt.close("all")
    plot_results(df)

    print("\nSimulation complete.")
    print("   Charts saved in results/")
