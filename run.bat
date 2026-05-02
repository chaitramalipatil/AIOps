@echo off
cd /d "%~dp0"
if not exist "%~dp0venv\Scripts\python.exe" (
  echo venv not found. Run: python -m venv venv ^&^& venv\Scripts\pip install -r requirements.txt
  exit /b 1
)
"%~dp0venv\Scripts\python.exe" -m streamlit run "%~dp0app.py" %*
