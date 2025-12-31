"""
Log Level explanation:
    Critical:   Errors where Program cannot continue running , example: duplicate keys in database
    Error:      Failure in a function that leads to that function not being able to complete.
    Warn:       Failure in the Program that needs to alert the user but not halt , example: connection failed to DB, retry possible
    Info:       General Purpose logs, "Start importing file xy , finished importing file xy" and so on.
    Debug:      Expands to log more frequently than Info, also with the file open at the time of logging.
    Trace:      Log EVERYTHING , what method is being called, what file is opened (...)
"""

import logging
import logging.config
from pathlib import Path
#TODO: Rewrite Logging
class AnsiColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord):
        no_style = '\033[0m'
        green = '\033[92m'
        bold = '\033[91m'
        grey = '\033[90m'
        yellow = '\033[93m'
        red = '\033[31m'
        red_light = '\033[91m'
        start_style = {
            'TRACE': grey,
            'DEBUG': no_style,
            'INFO': green,
            'WARNING': yellow,
            'ERROR': red,
            'CRITICAL': red_light + bold,
        }.get(record.levelname, no_style)
        end_style = no_style
        return f'{start_style}{super().format(record)}{end_style}'

def setup_logging(
    level: str = "INFO",
    log_dir: str | None = None,
    ) -> None:
    # Define Trace
    TRACE_LVL_NUM = 5
    logging.addLevelName(TRACE_LVL_NUM, "TRACE")
    def trace(self, message, *args, **kws):
        if self.isEnabledFor(TRACE_LVL_NUM):
            self._log(TRACE_LVL_NUM, message, args, **kws)
    logging.Logger.trace = trace


    # Define Logging
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = AnsiColorFormatter('{asctime} | {levelname:<8s} | {name:<20s} | {message}', style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
