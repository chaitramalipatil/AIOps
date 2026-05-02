$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot
$py = Join-Path $ProjectRoot "venv\Scripts\python.exe"
if (-not (Test-Path $py)) {
    Write-Error "venv not found. Run: python -m venv venv && .\venv\Scripts\pip install -r requirements.txt"
    exit 1
}
& $py -m streamlit run (Join-Path $ProjectRoot "app.py") @args
