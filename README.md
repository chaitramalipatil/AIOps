# AIOps — AI Support Assistant for IT Operations

AI-powered AIOps platform with chatbot-based incident analysis, root cause detection, and automated resolution workflows.

## Overview

This app streamlines IT operations by analyzing incidents, surfacing likely root causes, and suggesting resolution steps. It combines a **Streamlit** enterprise-style UI (dashboard, AI chat, simulated ServiceNow incidents, AIOps insights, automation, analytics) with optional **OpenAI** analysis.

---

## Key features

- **AI Chat Assistant** — Conversational triage with structured output: summary, root cause, resolution steps, confidence, related incidents (simulated).
- **Incidents (ServiceNow-style)** — Sample queue, detail pane, **Analyze with AI**.
- **AIOps insights** — Trends, categories, clustering-style chart, heatmap, recommendations (sample data).
- **Automation / utilities** — Simulated runbooks with status and logs.
- **Analytics** — SLA trend, automation impact, engineer throughput (sample data).

---

## Tech stack

- Python, Streamlit, Plotly, Pandas  
- OpenAI API (optional; **Demo mode** works offline)  
- `python-dotenv` for local secrets  

---

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/chaitramalipatil/AIOps.git
cd AIOps
```

### 2. Virtual environment and dependencies

```bash
python -m venv venv
```

**Windows:** `venv\Scripts\activate`  
**macOS/Linux:** `source venv/bin/activate`

```bash
pip install -r requirements.txt
```

### 3. API key (optional)

- Copy `.env.example` to `.env`
- Set `OPENAI_API_KEY` for live model calls  
- Or enable **Demo mode (no API)** in the app sidebar if you have no quota or key.

### 4. Run locally

**Windows (recommended):** from the project folder:

```powershell
.\run.ps1
```

Or:

```powershell
.\venv\Scripts\python.exe -m streamlit run app.py
```

If `streamlit` is “not found” from Conda `(base)`, use the project `venv` commands above.

---

## Use case

Built for IT support, L2/L3 operations, and AIOps engineers who want a credible demo or starting point for wiring real ServiceNow / observability APIs.
