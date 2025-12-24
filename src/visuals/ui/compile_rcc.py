#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QRC = ROOT / "ui" / "resources.qrc"
OUT = ROOT / "ui" / "generated_resources.py"

def main() -> int:
    if not QRC.exists():
        print(f"No QRC found at {QRC} (skip)")
        return 0
    cmd = ["pyside6-rcc", str(QRC), "-o", str(OUT)]
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"Generated resources into {OUT}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
