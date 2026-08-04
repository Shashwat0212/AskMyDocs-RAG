# Scripts Knowledge

## Current Contents

This folder contains Day Zero setup scripts:

- `setup_day_zero_macos.sh`
- `setup_day_zero_windows.ps1`

## Responsibilities

Scripts in this folder support local setup, future pinned Colab bootstrap/service lifecycle, experiment orchestration, and repository maintenance. They must preserve the runtime and artifact boundaries, remain reproducible, and not install application dependencies or pull models until an approved ticket owns that behavior.

## Update Notes

Update this file when scripts are added, removed, renamed, or given new behavior. Document any platform assumptions and validation commands in `docs/operations/`.
