"""
Log Level explanation:
    Critical:   Errors where Program cannot continue running , example: duplicate keys in database
    ERROR:      Failure in a function that leads to that function not being able to complete.
    WARN:       Failure in the Program that needs to alert the user but not halt , example: connection failed to DB, retry possible
    INFO:       General Purpose logs, "Start importing file xy , finished importing file xy" and so on.
    DEBUG:      Expands to log more frequently than Info, also with the file open at the time of logging.
    TRACE:      Log EVERYTHING , what method is being called, what file is opened (...)
"""

import logging
import logging.config
from pathlib import Path

def setup_logging(
    level: str = "INFO",
    log_dir: str | None = None,
    ) -> None:
    """
    central configuration for logging. \n
    hierarchie: DEBUG > INFO > WARNING > ERROR > CRITICAL

    Parameters
    ----------
    level : str 
        loglevel, which is wished
    log_dir : str | None
        directory for logfiles. off by default
    
    """
    handlers: dict = {
        "console": {
            "class": "logging.StreamHandler",
            "level": level,
            "formatter": "console",
            "stream": "ext://sys.stderr",
        }
    }

    if log_dir is not None:
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        handlers["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "level": level,
            "formatter": "file",
            "filename": str(Path(log_dir) / f"lsas.log"),
            "maxBytes": 10 * 1024 * 1024,  # 10MB
            "backupCount": 5,
            "encoding": "utf-8",
        }

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            },
            "file": {
                "format": "%(asctime)s %(levelname)s %(name)s "
                          "[%(process)d:%(threadName)s] %(message)s",
            },
        },
        "handlers": handlers,
        "root": {
            "level": level,
            "handlers": list(handlers.keys()),
        },
    }
    TRACE_LVL_NUM = 9
    logging.addLevelName(TRACE_LVL_NUM, "TRACE")
    def trace(self, message, *args, **kws):
        if self.isEnabledFor(TRACE_LVL_NUM):
            self._log(TRACE_LVL_NUM, message, args, **kws)
    logging.Logger.trace = trace
    logging.config.dictConfig(logging_config)
