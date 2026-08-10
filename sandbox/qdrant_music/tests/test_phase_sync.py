from __future__ import annotations

import json
from pathlib import Path

from qdrant_music.settings import PHASE_IDS, SETTINGS


def _notebook_text(path: Path) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    return "\n".join(
        "".join(cell.get("source", []))
        if isinstance(cell.get("source", []), list)
        else cell.get("source", "")
        for cell in notebook["cells"]
    )


def test_markdown_and_notebook_contain_every_phase() -> None:
    markdown_path = (
        SETTINGS.repository_root
        / "docs"
        / "tutorials"
        / "qdrant_billboard_walkthrough.md"
    )
    notebook_path = (
        SETTINGS.repository_root
        / "output"
        / "jupyter-notebook"
        / "qdrant_billboard_internals_tutorial.ipynb"
    )
    markdown = markdown_path.read_text(encoding="utf-8")
    notebook = _notebook_text(notebook_path)

    for phase_id in PHASE_IDS:
        assert f"## {phase_id} " in markdown
        assert f"## {phase_id} " in notebook


def test_notebook_is_clean_and_uses_expected_kernel() -> None:
    notebook_path = (
        SETTINGS.repository_root
        / "output"
        / "jupyter-notebook"
        / "qdrant_billboard_internals_tutorial.ipynb"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    assert notebook["metadata"]["kernelspec"]["name"] == "qdrant-music"
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            assert cell["execution_count"] is None
            assert cell["outputs"] == []


def test_executable_step_files_cover_q02_through_q16() -> None:
    steps_dir = (
        SETTINGS.repository_root
        / "sandbox"
        / "qdrant_music"
        / "src"
        / "qdrant_music"
        / "tutorial_steps"
    )
    available = {path.name[:3].upper() for path in steps_dir.glob("q[0-9][0-9]_*.py")}

    assert available == {f"Q{index:02d}" for index in range(2, 17)}
