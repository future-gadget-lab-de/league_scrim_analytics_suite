"""
Log Level explanation:
    Critical(50):   Errors where Program cannot continue running , example: duplicate keys in database
    Error(40):      Failure in a function that leads to that function not being able to complete.
    Warn(30):       Failure in the Program that needs to alert the user but not halt , example: connection failed to DB, retry possible
    Success(25):    Log succesful larger operations.
    Info(20):       General Purpose logs, "Start importing file xy , finished importing file xy" and so on.
    Debug(10):      Expands to log more frequently than Info, also with the file open at the time of logging.
    Trace(5):       Log EVERYTHING , what method is being called, what file is opened (...)
"""
import sys
from loguru import logger

def custom_format(record ):
    if record["level"].no >= 10:
        return "<red>{time}</> - {level} - <red>{thread}</> - <lvl>{message}</>\n{exception}"
    else:
        return "<green>{time}</> - {level} - <lvl>{message}</lvl>\n{exception}"
def setup_logging(
    level: str = "INFO",
    log_dir: str | None = None,
    ) -> None:
    # Clear definition
    logger.remove()
    logger.add(sys.stderr , level=level, format= custom_format)
