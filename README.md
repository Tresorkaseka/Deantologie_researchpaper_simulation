# Deantologie Research Paper Simulation

This repository studies organizational ethics through agent-based simulation. It combines Mesa, configurable LLM-based reasoning, scenario-driven experimentation, and research-oriented reporting to explore how peer influence, institutional strength, leadership, and pressure affect ethical behavior inside a technology organization.

## Overview

- Mesa-based simulation of ethical, unethical, neutral, and leadership profiles
- Four structural research scenarios designed for comparative analysis
- Provider-agnostic LLM adapter for qualitative agent justifications
- Research documentation covering execution, architecture, and the formal ODD model

## Research Design

The project models organizational behavior as a hybrid system:

- the simulation core governs movement, neighborhood effects, scores, and state transitions;
- the LLM layer provides short explanatory justifications for agent decisions;
- the reporting layer turns scenario outputs into readable research material.

This architecture keeps the transition logic explicit while adding an interpretable qualitative layer.

## LLM Configuration

The LLM runtime is intentionally provider-agnostic. Users can connect the provider that fits their needs, including Anthropic, OpenAI, or Gemini.

The adapter is isolated in `llm_backend.py`, so provider changes do not require rewriting the simulation core. A typical configuration uses:

```ini
LLM_PROVIDER=
LLM_MODEL_NAME=provider/model-name
LLM_API_KEY=your_api_key
LLM_BASE_URL=
```

Example model identifiers:

- `openai/gpt-4o-mini`
- `anthropic/claude-3-7-sonnet-latest`
- `gemini/gemini-2.0-flash`

## Quick Start

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
.\venv\Scripts\python.exe run_research_experiments.py
```

## Main Commands

```bash
.\venv\Scripts\python.exe run_simple.py
.\venv\Scripts\python.exe run.py
.\venv\Scripts\python.exe run_research_experiments.py
.\venv\Scripts\python.exe build_full_report.py
.\venv\Scripts\python.exe vis_server.py
```

## Repository Structure

- `agents.py`: agent behavior and decision flow
- `model.py`: Mesa model, scheduler, grid, and metrics
- `llm_backend.py`: provider-facing LLM adapter
- `research_config.py`: structural experiment definitions
- `run_research_experiments.py`: full campaign orchestration
- `viz.py`: charts, grids, and visual evidence
- `build_full_report.py`: research report assembly
- `docs/`: project documentation and architecture references

## Documentation

- [Execution Guide](docs/Execution_Guide.md)
- [Project Architecture](docs/Project_Architecture.md)
- [Code Architecture](docs/Code_Architecture.md)
- [ODD Documentation](docs/ODD_Documentation.md)
- [Maintenance and Launch Guide](docs/Maintenance_et_Lancement.md)
