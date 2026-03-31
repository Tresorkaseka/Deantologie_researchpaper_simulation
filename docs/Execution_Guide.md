# Execution Guide

## 1. Project goal

This repository simulates ethical decision-making dynamics inside a technology organization through agent-based modeling, qualitative agent reasoning, and research-oriented reporting.

## 2. What you need

- Python 3.11 or newer
- Windows PowerShell
- Microsoft Edge for PDF generation
- Access to the model provider you want to use

You can connect the provider and model of your choice, for example Anthropic, OpenAI, or Gemini.

## 3. Installation

### 3.1 Create the virtual environment

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3.2 Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure the LLM layer

### 4.1 Create the environment file

Use `.env.example` as the template and create `.env` at the repository root:

```ini
LLM_PROVIDER=
LLM_MODEL_NAME=provider/model-name
LLM_API_KEY=your_api_key
LLM_BASE_URL=
```

Recommended model name examples:

- `openai/gpt-4o-mini`
- `anthropic/claude-3-7-sonnet-latest`
- `gemini/gemini-2.0-flash`

Leave `LLM_PROVIDER` empty if the model name already includes the provider prefix. Use `LLM_BASE_URL` only when the chosen backend exposes an OpenAI-compatible endpoint.

### 4.2 Adjust the adapter if needed

The file `llm_backend.py` is the generic connection point for the LLM layer. The current implementation uses LiteLLM so users can select a supported provider through configuration instead of changing the simulation code.

## 5. Run the project

### 5.1 Quick run

```bash
.\venv\Scripts\python.exe run_simple.py
```

Use this when you want a short validation run with a small number of agents and ticks.

### 5.2 Standard simulation run

```bash
.\venv\Scripts\python.exe run.py
```

Use this when you want a standard single-run simulation with chart generation.

### 5.3 Full research campaign

```bash
.\venv\Scripts\python.exe run_research_experiments.py
```

This command runs the four structural scenarios and generates:

- per-scenario metrics;
- quantitative charts;
- conversation logs;
- conversation snapshots;
- initial and final grids;
- a global summary CSV.

## 6. Generate the documentation package

### 6.1 Rebuild generated Markdown reports

```bash
.\venv\Scripts\python.exe build_full_report.py
```

### 6.2 Generate the PDF set

```bash
.\venv\Scripts\python.exe docs\generate_pdf.py
```

This command renders every Markdown document in `docs/` into a PDF version. Mermaid architecture diagrams are rendered visually during the export.

## 7. Launch the browser visualization

```bash
.\venv\Scripts\python.exe vis_server.py
```

Then open `http://localhost:8521`.

## 8. Verify the setup

### 8.1 Dependency check

```bash
.\venv\Scripts\python.exe verify_setup.py
```

### 8.2 LLM backend check

```bash
.\venv\Scripts\python.exe test_connection.py
```

## 9. Output locations

- Generated scenario outputs: `results/`
- Generated research reports: `docs/Rapport_Recherche_Simulations.md`, `docs/Rapport_Complet_Simulations.md`, `docs/Documentation_Projet.md`
- Public PDF documentation set: `docs/*.pdf`

Generated research reports can be rebuilt at any time. The public documentation PDFs can be regenerated whenever the Markdown sources change.

## 10. Recommended workflow for GitHub

1. Keep only source files and hand-written documentation under version control.
2. Exclude `.env`, `results/`, internal working folders, logs, caches, and temporary HTML exports.
3. Regenerate reports locally when you need them instead of committing them.
4. Commit the source code, documentation sources, and configuration templates.
