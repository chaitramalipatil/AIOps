# AI Support Assistant (AIOps Chatbot)

## Overview

AI-powered assistant designed for IT support engineers to analyze issues and suggest resolutions.

## Features

- Issue summarization
- Root cause analysis
- Suggested resolution steps
- Interactive UI using Streamlit

## Tech Stack

- Python
- OpenAI API
- Streamlit

## Setup

1. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   ```

2. Activate it:

   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure your API key:

   - Copy `.env.example` to `.env`
   - Set `OPENAI_API_KEY` to your key

## Run locally

**Windows (recommended):** from this folder, double-click `run.bat` or in PowerShell:

```powershell
.\run.ps1
```

That uses the project `venv` so you do not need `streamlit` on your global or Conda PATH.

**If you use `venv` manually:**

```powershell
.\venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

**Why `streamlit` was not found:** Streamlit is installed inside `venv`. Conda `(base)` does not include it unless you also `conda install streamlit` there. Prefer the project venv above.

## Use case

Helps reduce manual effort in IT operations by providing instant AI-driven insights.
