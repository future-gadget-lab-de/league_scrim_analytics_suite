"""
entrypoint for all GUI Applications
"""
import subprocess, pathlib, sys,logging
from PySide6.QtWidgets import QApplication
LSAS = pathlib.Path(__file__).resolve().parents[3]
COMPILE_UI = LSAS / "LSAS" / "src" / "visuals" / "ui" 
from loguru import logger
def runAdvancedFrontend() -> None:
    logger.trace("Started runAdvancedFrontend Function.")
    try:
        from src.visuals.windows.main_window import MainWindow
    except:
        try:
            logger.info("Compiling UI.")
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
