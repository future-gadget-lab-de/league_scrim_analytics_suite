#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMS_DIR = ROOT / "ui" / "forms"
OUT_DIR = ROOT / "ui" / "generated"

def main() -> int:
    if not FORMS_DIR.exists():
        raise SystemExit(f"Forms directory not found: {FORMS_DIR}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "__init__.py").touch(exist_ok=True)

    uis = sorted(FORMS_DIR.glob("*.ui"))
    if not uis:
        print(f"No .ui files found in {FORMS_DIR}")
        return 0

    for ui in uis:
        out_py = OUT_DIR / f"ui_{ui.stem}.py"
        cmd = ["./.venv/bin/pyside6-uic", str(ui), "-o", str(out_py)]
        print(" ".join(cmd))
        subprocess.run(cmd, check=True)

    print(f"Generated {len(uis)} UI file(s) into {OUT_DIR}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
