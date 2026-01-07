#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path
from loguru import logger
ROOT = Path(__file__).resolve().parents[1]
QRC = ROOT / "ui" / "resources.qrc"
OUT = ROOT / "ui" / "generated_resources.py"

def main() -> int:
    logger.debug("RCC Compile Start")
    if not QRC.exists():
        # print(f"No QRC found at {QRC} (skip)")
        logger.info("No QRC found at " + str(QRC))
        return 0
    cmd = ["pyside6-rcc", str(QRC), "-o", str(OUT)]
    #print(" ".join(cmd)) HACK: Wieso ist das da ??? 
    subprocess.run(cmd, check=True)
    logger.debug("Generated ressources into " + str(OUT))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
