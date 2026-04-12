from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib

# Ensure plotting works reliably in headless/CI contexts on Windows.
matplotlib.use("Agg")

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from agents import ProfessionalAgent, TYPE_COLORS


RESULTS_DIR = Path(__file__).resolve().parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def hex_to_rgb(hex_color: str) -> list[float]:
    value = hex_color.lstrip("#")
    return [int(value[index:index + 2], 16) / 255 for index in (0, 2, 4)]


def draw_grid(model, tick: int, output_path: str | Path | None = None, title: str | None = None):
    grid_size = model.grid.width
    grid_data = np.zeros((grid_size, grid_size, 3))
    grid_data[:] = [0.96, 0.97, 0.98]

    for cell_content, (x, y) in model.grid.coord_iter():
        agents = [agent for agent in cell_content if isinstance(agent, ProfessionalAgent)]
        if agents:
            grid_data[y][x] = hex_to_rgb(TYPE_COLORS[agents[0].agent_type])

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(grid_data, origin="lower", interpolation="nearest")
    ax.set_title(title or f"Organization - observation {tick}", fontsize=13, fontweight="bold")
    ax.set_xlabel("X position")
    ax.set_ylabel("Y position")
    ax.grid(False)

    legend = [
        mpatches.Patch(color=TYPE_COLORS["ethical"], label="Ethical"),
        mpatches.Patch(color=TYPE_COLORS["non_ethical"], label="Unethical"),
        mpatches.Patch(color=TYPE_COLORS["neutral"], label="Neutral"),
        mpatches.Patch(color=TYPE_COLORS["leader"], label="Leader"),
        mpatches.Patch(color=TYPE_COLORS["toxic_leader"], label="Toxic leader"),
    ]
    ax.legend(handles=legend, loc="upper right", fontsize=9, frameon=True)
    fig.tight_layout()

    if output_path is not None:
        fig.savefig(output_path, dpi=180, bbox_inches="tight")
        plt.close(fig)
    return fig


def plot_scenario_metrics(
    df: pd.DataFrame,
    scenario_title: str,
    output_path: str | Path,
) -> None:
    ticks = list(range(len(df)))
    fig, axes = plt.subplots(1, 2, figsize=(13.8, 5.2))

    axes[0].plot(
        ticks,
        df["Ethical"],
        color=TYPE_COLORS["ethical"],
        linewidth=2.4,
        marker="o",
        label="Ethical",
    )
    axes[0].plot(
        ticks,
        df["NonEthical"],
        color=TYPE_COLORS["non_ethical"],
        linewidth=2.4,
        marker="o",
        label="Unethical",
    )
    axes[0].plot(
        ticks,
        df["Neutral"],
        color=TYPE_COLORS["neutral"],
        linewidth=2.0,
        marker="o",
        label="Neutral",
    )
    axes[0].plot(
        ticks,
        df["Leader"],
        color=TYPE_COLORS["leader"],
        linewidth=2.0,
        marker="o",
        linestyle="--",
        label="Leaders",
    )
    axes[0].set_title("Behavioral composition")
    axes[0].set_xlabel("Observation")
    axes[0].set_ylabel("Number of agents")
    axes[0].grid(True, alpha=0.25)
    axes[0].legend(frameon=False)

    axes[1].plot(ticks, df["EthicalRatio"], color="#146c43", linewidth=2.6, marker="o")
    axes[1].fill_between(ticks, df["EthicalRatio"], color="#74c69d", alpha=0.28)
    axes[1].axhline(y=0.5, color="#6c757d", linestyle="--", linewidth=1.2)
    axes[1].text(
        0.05,
        0.52,
        "ethical majority threshold",
        transform=axes[1].transAxes,
        fontsize=9,
        color="#6c757d",
    )
    axes[1].set_title("Ethical ratio trajectory")
    axes[1].set_xlabel("Observation")
    axes[1].set_ylabel("Ratio (0 to 1)")
    axes[1].set_ylim(0, 1.05)
    axes[1].grid(True, alpha=0.25)

    fig.suptitle(f"{scenario_title} - Quantitative results", fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_comparative_metrics(
    scenario_frames: dict[str, pd.DataFrame],
    scenario_titles: dict[str, str],
    output_path: str | Path,
) -> None:
    fig, ax = plt.subplots(figsize=(10.8, 6.0))
    styles = {
        # NOTE: We deliberately vary line styles/markers so that scenarios that
        # end up with identical trajectories (e.g., a flat 0.4 line) remain
        # visually distinguishable in the comparative figure.
        "A_Peur": {"color": "#b42318", "linestyle": "--", "marker": "s", "zorder": 4},
        "B_Forteresse": {"color": "#157347", "linestyle": "-", "marker": "o", "zorder": 3},
        "C_Crise": {"color": "#b26a00", "linestyle": "-", "marker": "D", "zorder": 2},
        "D_Bulle": {"color": "#5b3cc4", "linestyle": "-.", "marker": "^", "zorder": 2},
    }

    preferred_order = ("A_Peur", "B_Forteresse", "C_Crise", "D_Bulle")
    slugs = [slug for slug in preferred_order if slug in scenario_frames]
    slugs.extend(slug for slug in scenario_frames.keys() if slug not in slugs)

    for slug in slugs:
        df = scenario_frames[slug]
        ticks = list(range(len(df)))
        style = styles.get(slug, {"color": "#123b5d", "linestyle": "-", "marker": "o", "zorder": 2})
        ax.plot(
            ticks,
            df["EthicalRatio"],
            linewidth=2.5,
            linestyle=style["linestyle"],
            marker=style["marker"],
            markersize=7,
            markeredgecolor="#ffffff",
            markeredgewidth=0.8,
            color=style["color"],
            zorder=style["zorder"],
            label=scenario_titles.get(slug, slug),
        )

    ax.axhline(y=0.5, color="#6c757d", linestyle="--", linewidth=1.2)
    ax.set_title("Cross-scenario comparison of the ethical ratio", fontsize=14, fontweight="bold")
    ax.set_xlabel("Observation")
    ax.set_ylabel("Ethical ratio")
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_results(df: pd.DataFrame, output_path: str | Path | None = None) -> None:
    output_path = Path(output_path) if output_path is not None else RESULTS_DIR / "evolution_ethique.png"
    plot_scenario_metrics(df, "Simulation run", output_path)


def render_conversation_snapshot(
    title: str,
    lines: list[str],
    output_path: str | Path,
    subtitle: str | None = None,
) -> None:
    wrapped_lines: list[str] = []
    for line in lines:
        wrapped_lines.extend(
            textwrap.wrap(
                line,
                width=86,
                break_long_words=False,
                break_on_hyphens=False,
            )
            or [""]
        )

    content = "\n".join(wrapped_lines[:42])
    fig = plt.figure(figsize=(11.0, 8.4), facecolor="#f8fafc")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()

    ax.text(0.04, 0.96, title, fontsize=16, fontweight="bold", color="#123b5d", va="top")
    if subtitle:
        ax.text(0.04, 0.92, subtitle, fontsize=10, color="#52606d", va="top")

    ax.text(
        0.04,
        0.87,
        content,
        family="monospace",
        fontsize=9.3,
        color="#1f2933",
        va="top",
        linespacing=1.33,
        bbox={
            "facecolor": "#ffffff",
            "edgecolor": "#d9e2ec",
            "boxstyle": "round,pad=0.7",
        },
    )
    fig.savefig(output_path, dpi=220, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
