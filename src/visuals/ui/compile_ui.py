#!/usr/bin/env python3
from __future__ import annotations

import platform
import subprocess
from pathlib import Path
import os
from loguru import logger

ROOT = Path(__file__).resolve().parents[1]
LSAS = Path(__file__).resolve().parents[3]
FORMS_DIR = ROOT / "ui" / "forms"
OUT_DIR = ROOT / "ui" / "generated"

def find_file_in_path(base_abs_path: str, target_filename: str) -> str: #NOTE: Gehört das nicht in Utils eig. ? #NOTE: Nein.
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
    logger.trace("Started find_file_in_path Function with base_abs_path: " + base_abs_path +" and target_filename: " + target_filename)
    if not os.path.isabs(base_abs_path):
        err_msg = "Base path must be absolute"
        logger.error(err_msg)
        raise ValueError(err_msg)
    if not os.path.isdir(base_abs_path):
        err_msg = "Base directory not found: "+base_abs_path
        logger.error(err_msg)
        raise FileNotFoundError(err_msg)

    for root, _, files in os.walk(base_abs_path):
        if target_filename in files:
            return os.path.join(root, target_filename)
    err_msg = "File "+ target_filename +" not found under: " + base_abs_path
    logger.error(err_msg)
    raise FileNotFoundError(err_msg)


def main() -> int:

    logger.trace("Start compile_ui.py")
    if platform.system() == "Windows":
        binary = find_file_in_path(str(LSAS), "pyside6-uic.exe")
    else:
        binary = find_file_in_path(str(LSAS), "pyside6-uic")

    logger.trace("Checking existence of Forms Directory")
    if not FORMS_DIR.exists():
        err_msg = "Forms directory not found: "+ str(FORMS_DIR)
        logger.critical(err_msg)
        raise SystemExit(err_msg)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "__init__.py").touch(exist_ok=True)

    uis = sorted(FORMS_DIR.glob("*.ui"))
    logger.trace("Checking if ui files exist.")
    if not uis:
        logger.error("No .ui files found in" + str(FORMS_DIR))
        return 0
    for ui in uis:
        out_py = OUT_DIR / f"ui_{ui.stem}.py"
        try:
            logger.trace("Compiling: "+str(ui))
            cmd = [binary, str(ui), "-o", str(out_py)]
            subprocess.run(cmd, check=True)
        except:
            err_msg = "Your pyside6 installation isnt inside a venv."
            logger.critical(err_msg)
            raise FileNotFoundError(err_msg)

    logger.info("Generated: "+ str(len(uis)) + "UI files into " +str(OUT_DIR))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
