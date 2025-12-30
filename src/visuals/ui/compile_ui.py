#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
LSAS = Path(__file__).resolve().parents[3]
FORMS_DIR = ROOT / "ui" / "forms"
OUT_DIR = ROOT / "ui" / "generated"


def find_file_in_path(base_abs_path: str, target_filename: str) -> str:
    """
    Searches recursively for a file name within an absolute base path and returns its absolute path.

    Parameters
    ----------
    base_abs_path : str
        Absolute path to the directory to search in.
    target_filename : str
        Name of the file to look for.

    Returns
    -------
    str
        Absolute path of the first matching file.

    Raises
    ------
    ValueError
        If the provided base path is not absolute.
    FileNotFoundError
        If the base directory does not exist or the file is not found.
    """
    if not os.path.isabs(base_abs_path):
        raise ValueError("Base path must be absolute")
    if not os.path.isdir(base_abs_path):
        raise FileNotFoundError(f"Base directory not found: {base_abs_path}")

    for root, _, files in os.walk(base_abs_path):
        if target_filename in files:
            return os.path.join(root, target_filename)

    raise FileNotFoundError(f"File '{target_filename}' not found under '{base_abs_path}'")


def main() -> int:

    binary = find_file_in_path(str(LSAS), "pyside6-uic")

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
        try:
            cmd = [binary, str(ui), "-o", str(out_py)]
            print(" ".join(cmd))
            subprocess.run(cmd, check=True)
        except:
            raise FileNotFoundError("Your pyside6 installation isnt inside a venv.")
            
    print(f"Generated {len(uis)} UI file(s) into {OUT_DIR}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
