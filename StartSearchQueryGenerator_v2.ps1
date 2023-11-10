$scriptName = "SearchQuerygeneratorWithUi_ChatGPT_v8.py"
# Get the directory of the script being executed
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path

# Specify the relative paths to your Python executable and virtual environment
$pythonExecutable = Join-Path $scriptDirectory ".venv\Scripts\python.exe"
$virtualEnvPath = Join-Path $scriptDirectory ".venv"

# Activate the virtual environment
$activateScript = Join-Path $virtualEnvPath "Scripts\Activate"
if (Test-Path $activateScript) {
    Write-Host "Activating virtual environment..."
    & $activateScript
} else {
    Write-Host "Virtual environment activation script not found."
}

# Run the main.py file using the activated Python environment
if (Test-Path $pythonExecutable) {
    $mainScript = Join-Path $scriptDirectory $scriptName
    if (Test-Path $mainScript) {
        Write-Host "Running Search Query Generator..."
        & $pythonExecutable $mainScript
    } else {
        Write-Host "$scriptName file not found."
    }
} else {
    Write-Host "Python executable not found."
}