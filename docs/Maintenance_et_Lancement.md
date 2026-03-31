# Maintenance and launch guide

## 1. Purpose

This document explains how to rerun the scenarios, regenerate the reports, and maintain the project for research and publication workflows.

## 2. Prerequisites

### 2.1 Environment

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2.2 Environment variables

Create a `.env` file at the repository root:

```ini
LLM_PROVIDER=
LLM_MODEL_NAME=provider/model-name
LLM_API_KEY=your_api_key
LLM_BASE_URL=
```

You can connect the model provider you want, for example Anthropic, OpenAI, or Gemini. Recommended model identifiers are `openai/gpt-4o-mini`, `anthropic/claude-3-7-sonnet-latest`, or `gemini/gemini-2.0-flash`. The repository excludes `.env` through `.gitignore`.

### 2.3 LLM adapter

The project exposes a generic LLM entry point in `llm_backend.py`. The current adapter uses LiteLLM, which means most users can switch providers through environment variables alone. If a future backend is not covered, this is the only file that should need adaptation.

## 3. Recommended execution chain

### 3.1 Rerun the scenarios

```bash
.\venv\Scripts\python.exe run_research_experiments.py
```

This command:

1. runs the four research scenarios;
2. creates one `results/scenarios/<slug>/` subfolder per scenario;
3. generates metric tables, charts, conversation excerpts, and grids;
4. updates `results/scenario_summary.csv` and `results/graph_papier_recherche.png`.

### 3.2 Rebuild the Markdown documents

```bash
.\venv\Scripts\python.exe build_full_report.py
```

This command regenerates:

- `docs/Rapport_Recherche_Simulations.md`
- `docs/Rapport_Complet_Simulations.md`
- `docs/Documentation_Projet.md`

These files are generated artifacts and are intentionally excluded from version control.

## 4. Maintenance advice

### 4.1 Before a new campaign

Check:

1. that the API key is valid;
2. that the virtual environment includes the packages from `requirements.txt`;
3. that the selected provider/model pair is reflected in `.env`.

### 4.2 If the output seems inconsistent

- Re-read `results/scenario_summary.csv`.
- Check each scenario log.
- Verify whether transient LLM errors or rate limiting disrupted the campaign.
- Rerun the experiments if the qualitative traces are not satisfactory.

### 4.3 If the documentation must be enriched

The best entry points are:

- `research_config.py` for scenario hypotheses and descriptions;
- `build_full_report.py` for document structure;
- `viz.py` for visuals;
- `docs/Execution_Guide.md` for onboarding and usage instructions.

## 5. Academic usage

For a dissertation or article, the recommended chain is:

1. rerun the scenarios;
2. inspect the per-scenario artifacts;
3. rebuild the Markdown files;
4. review the main report and appendices before sharing.

## 6. End-to-end command chain

```bash
.\venv\Scripts\python.exe run_research_experiments.py
.\venv\Scripts\python.exe build_full_report.py
```
