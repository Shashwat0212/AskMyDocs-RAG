$ErrorActionPreference = "Stop"

# Update PATH to include newly installed tools from winget
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
$oligmaPath = "$env:USERPROFILE\AppData\Local\Programs\Ollama"
if (Test-Path $oligmaPath) {
    $env:Path = "$oligmaPath;$env:Path"
}
# Check for GnuWin32 in both common locations
$gnuWin32Paths = @("C:\Program Files (x86)\GnuWin32\bin", "C:\GnuWin32\bin")
foreach ($gnuWin32Path in $gnuWin32Paths) {
    if (Test-Path $gnuWin32Path) {
        $env:Path = "$gnuWin32Path;$env:Path"
        break
    }
}

function Fail-DayZero {
    param([string]$Message)
    Write-Host ""
    Write-Host "FAILED: $Message" -ForegroundColor Red
    Write-Host "Stop here. Create a Jira ticket titled 'Day Zero Environment Issue'."
    Write-Host "Include the failed command, terminal output, Windows version, and any fix attempted."
    exit 1
}

function Run-Step {
    param(
        [string]$Label,
        [scriptblock]$Command
    )
    Write-Host ""
    Write-Host "==> $Label" -ForegroundColor Cyan
    try {
        & $Command
    }
    catch {
        Fail-DayZero "$Label :: $($_.Exception.Message)"
    }
}

function Has-Command {
    param([string]$Name)
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Install-WingetPackage {
    param(
        [string]$Id,
        [string]$Name
    )
    Run-Step "Install $Name" {
        winget install --id $Id -e --accept-source-agreements --accept-package-agreements
    }
}

Write-Host "Day Zero Windows setup"
Write-Host "This installs machine tools only. It does not install app dependencies or pull models."

if (-not (Has-Command winget)) {
    Fail-DayZero "winget is missing. Install App Installer from Microsoft Store, reopen PowerShell, and rerun."
}

if (-not (Has-Command git)) {
    Install-WingetPackage "Git.Git" "Git"
}

if (-not (Has-Command py)) {
    Install-WingetPackage "Python.Python.3.11" "Python 3.11"
}

Run-Step "Verify Python 3.11" { py -3.11 --version }

if (-not (Has-Command uv)) {
    Run-Step "Install uv" {
        powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"
    }
    $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
}

if (-not (Has-Command node)) {
    Install-WingetPackage "OpenJS.NodeJS.LTS" "Node.js LTS"
}

if (-not (Has-Command pnpm)) {
    Run-Step "Enable pnpm through Corepack" {
        corepack enable
        corepack prepare pnpm@latest --activate
    }
}

if (-not (Has-Command docker)) {
    Install-WingetPackage "Docker.DockerDesktop" "Docker Desktop"
}

if (-not (Has-Command ollama)) {
    Install-WingetPackage "Ollama.Ollama" "Ollama"
}

if (-not (Has-Command jq)) {
    Install-WingetPackage "jqlang.jq" "jq"
}

if (-not (Has-Command wget)) {
    Install-WingetPackage "JernejSimoncic.Wget" "wget"
}

if (-not (Has-Command make)) {
    Install-WingetPackage "GnuWin32.Make" "make"
}

Run-Step "Verify Git" { git --version }
Run-Step "Verify Python 3.11 pip" { py -3.11 -m pip --version }
Run-Step "Verify Python 3.11 venv" { py -3.11 -m venv --help | Select-Object -First 1 }
Run-Step "Verify uv" { uv --version }
Run-Step "Verify Node" { node --version }
Run-Step "Verify npm" { npm --version }
Run-Step "Verify pnpm" { pnpm --version }
Run-Step "Verify curl" { curl.exe --version }
Run-Step "Verify wget" { wget.exe --version }
Run-Step "Verify make" { make --version }
Run-Step "Verify tar archive tooling" { tar --version }
Run-Step "Verify jq" { jq --version }

if (-not (Test-Path ".venv")) {
    Run-Step "Create .venv" { py -3.11 -m venv .venv }
}

Run-Step "Verify .venv Python" { .\.venv\Scripts\python.exe --version }
Run-Step "Verify .venv pip" { .\.venv\Scripts\python.exe -m pip --version }

Run-Step "Verify Docker CLI" { docker --version }
Run-Step "Verify Docker Compose" { docker compose version }

try {
    docker info | Out-Null
}
catch {
    Write-Host ""
    Write-Host "Docker is installed but the daemon is not reachable."
    Write-Host "Open Docker Desktop from the Start menu, wait until it finishes starting, then rerun this script."
    Fail-DayZero "Docker daemon not ready"
}

Run-Step "Verify Ollama CLI" { ollama --version }

try {
    ollama list | Out-Null
}
catch {
    Write-Host ""
    Write-Host "Ollama is installed but not reachable."
    Write-Host "Start Ollama from the Start menu or run: ollama serve"
    Write-Host "Then rerun this script."
    Fail-DayZero "Ollama server not reachable"
}

Run-Step "List Ollama models without pulling" { ollama list }

Write-Host ""
Write-Host "Day Zero Windows setup validation passed." -ForegroundColor Green
Write-Host "No project app dependencies were installed and no models were pulled."
