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

```bash
streamlit run app.py
```

## Use case

Helps reduce manual effort in IT operations by providing instant AI-driven insights.
