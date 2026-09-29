#!/usr/bin/env python3
"""Bootstrap a local venv for the knowledge-source-converter skill."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENV = ROOT / ".venv"
REQ = ROOT / "requirements.txt"


def run(cmd, **kwargs):
    print(f"> {' '.join(str(c) for c in cmd)}")
    subprocess.run(cmd, check=True, **kwargs)


def main():
    if not VENV.exists():
        run([sys.executable, "-m", "venv", str(VENV)])

    pip = VENV / "Scripts" / "python.exe" if os.name == "nt" else VENV / "bin" / "python"
    run([str(pip), "-m", "pip", "install", "--upgrade", "pip", "--quiet"])
    run([str(pip), "-m", "pip", "install", "-r", str(REQ), "--quiet"])
    print("Setup complete.")


if __name__ == "__main__":
    main()
