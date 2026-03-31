# Deantologie Research Paper Simulation

An agent-based research project that explores organizational ethics through simulation, qualitative agent reasoning, and research-grade documentation in both Markdown and PDF formats.

## What this repository contains

- a Mesa-based agent simulation of ethical and unethical behavior inside a tech organization;
- four structural research scenarios;
- a reporting pipeline for Markdown and PDF documentation outputs;
- maintenance, ODD, and execution documentation written in English.

## LLM layer

The LLM layer is intentionally provider-agnostic. You can connect the model provider you want, for example Anthropic, OpenAI, or Gemini.

The repository exposes a single adapter entry point in `llm_backend.py`, powered by LiteLLM, so the rest of the codebase can stay unchanged when you switch providers. If a future user wants an unsupported backend, only that adapter needs to be extended.

## Quick start

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
.\venv\Scripts\python.exe run_research_experiments.py
```

Use a model identifier such as `openai/gpt-4o-mini`, `anthropic/claude-3-7-sonnet-latest`, or `gemini/gemini-2.0-flash`.

## Main commands

```bash
.\venv\Scripts\python.exe run_simple.py
.\venv\Scripts\python.exe run.py
.\venv\Scripts\python.exe run_research_experiments.py
.\venv\Scripts\python.exe build_full_report.py
.\venv\Scripts\python.exe docs\generate_pdf.py
.\venv\Scripts\python.exe vis_server.py
```

## Documentation

- [Execution Guide](docs/Execution_Guide.md)
- [Project Architecture](docs/Project_Architecture.md)
- [Code Architecture](docs/Code_Architecture.md)
- [ODD Documentation](docs/ODD_Documentation.md)
- [Maintenance and Launch Guide](docs/Maintenance_et_Lancement.md)

Each public document can also be exported to PDF through `docs/generate_pdf.py`.

## Repository hygiene

This repository is set up to keep generated outputs out of version control. Reports, results, caches, logs, internal memory folders, and local secrets stay out of the public GitHub surface.
