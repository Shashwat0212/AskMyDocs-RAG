#!/usr/bin/env bash
set -euo pipefail

fail() {
  echo
  echo "FAILED: $1"
  echo "Stop here. Create a Jira ticket titled 'Day Zero Environment Issue'."
  echo "Include the failed command, terminal output, macOS version, and any fix attempted."
  exit 1
}

run() {
  echo
  echo "==> $*"
  "$@" || fail "$*"
}

has() {
  command -v "$1" >/dev/null 2>&1
}

echo "Day Zero macOS setup"
echo "This installs machine tools only. It does not install app dependencies or pull models."

if ! has brew; then
  echo
  echo "Homebrew is missing. Installing Homebrew from the official installer."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || fail "install Homebrew"
fi

run brew --version

if ! has git; then
  run brew install git
fi

if ! has python3.11; then
  run brew install python@3.11
fi

if ! has uv; then
  run brew install uv
fi

if ! node --version >/dev/null 2>&1; then
  run brew install node@24
  run brew link node@24 --force --overwrite
else
  node_major="$(node --version | sed 's/^v//' | cut -d. -f1)"
  if [ "$node_major" != "24" ]; then
    run brew install node@24
    brew unlink node >/dev/null 2>&1 || true
    run brew link node@24 --force --overwrite
  fi
fi

if ! has pnpm; then
  run brew install pnpm
fi

if ! has docker; then
  run brew install --cask docker
fi

if ! has ollama; then
  run brew install ollama
fi

if ! has wget; then
  run brew install wget
fi

if ! has jq; then
  run brew install jq
fi

run git --version
run python3.11 --version
run python3.11 -m pip --version
run python3.11 -m venv --help
run uv --version
run node --version
run npm --version
run pnpm --version
run curl --version
run wget --version
run make --version
run jq --version
run unzip -v

if [ ! -d ".venv" ]; then
  run python3.11 -m venv .venv
fi

run .venv/bin/python --version
run .venv/bin/python -m pip --version

echo
echo "Checking Docker Desktop."
if ! docker info >/dev/null 2>&1; then
  echo "Docker is installed but the daemon is not reachable."
  echo "Opening Docker Desktop. Wait until it finishes starting, then rerun this script."
  open -a Docker || fail "open Docker Desktop"
  fail "Docker daemon not ready"
fi

run docker --version
run docker compose version

echo
echo "Checking Ollama."
if ! ollama list >/dev/null 2>&1; then
  echo "Ollama is installed but not reachable."
  echo "Start it in another terminal with: ollama serve"
  echo "Then rerun this script."
  fail "Ollama server not reachable"
fi

run ollama --version
run ollama list

echo
echo "Day Zero macOS setup validation passed."
echo "No project app dependencies were installed and no models were pulled."
