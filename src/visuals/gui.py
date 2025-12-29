"""
entrypoint for all GUI Applications
"""

import subprocess, pathlib, sys
from src.visuals.windows.main_window import MainWindow
from PySide6.QtWidgets import QApplication

LSAS = pathlib.Path(__file__).resolve().parents[1]
COMPILE_UI = LSAS / "LSAS" / "src" / "visuals" / "ui" 

def runAdvancedFrontend() -> None:
    try:
        cmd = ["python3", str(COMPILE_UI) + "/compile_ui.py"]
        print(" ".join(cmd))
        subprocess.run(cmd, check=True)
    except:
        raise Exception("Something went off, while compiling the ui")
        sys.exit(1)
        
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())