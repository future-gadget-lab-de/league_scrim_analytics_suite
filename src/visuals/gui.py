"""
entrypoint for all GUI Applications
"""
#TODO: Rewrite Logging
import subprocess, pathlib, sys
from PySide6.QtWidgets import QApplication

LSAS = pathlib.Path(__file__).resolve().parents[3]
COMPILE_UI = LSAS / "LSAS" / "src" / "visuals" / "ui" 

def runAdvancedFrontend() -> None:

    try:
        from src.visuals.windows.main_window import MainWindow
    except:
        try:
            cmd = ["python3", str(COMPILE_UI) + "/compile_ui.py"]
            print(" ".join(cmd))
            subprocess.run(cmd, check=True)

            from src.visuals.windows.main_window import MainWindow
        except:
            raise Exception("Something went off, while compiling the ui")
            sys.exit(1)


    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
