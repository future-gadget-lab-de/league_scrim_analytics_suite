"""
entrypoint for all GUI Applications
"""
import subprocess, pathlib, sys, logging, platform
from PySide6.QtWidgets import QApplication
from loguru import logger
from src.core.config import config

LSAS = pathlib.Path(__file__).resolve().parents[3]
COMPILE_UI = LSAS / "LSAS" / "src" / "visuals" / "ui" 

def runAdvancedFrontend() -> None:
    """entrypoint method for all GUI applications"""
    
    logger.trace("Started runAdvancedFrontend Function.")
    from src.visuals.windows.main_window import MainWindow
    try:
        from src.visuals.windows.main_window import MainWindow
    except:
        try:
            logger.info("Compiling UI.")
            match platform.system():
                case "Windows":
                    binary = "./.venv/Scripts/python.exe"
                case "Linux":
                    binary = "./.venv/bin/python"

            cmd = [binary, str(COMPILE_UI) + "/compile_ui.py"]
            subprocess.run(cmd, check=True)

            from src.visuals.windows.main_window import MainWindow
        except Exception as e:
            raise Exception("Something went off, while compiling the ui"+ str(e))
            sys.exit(1)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    if app.exec():
        config.writeSettings()
