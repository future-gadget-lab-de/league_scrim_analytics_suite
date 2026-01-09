"""
Log Level explanation:
    - Critical(50):   Errors where Program cannot continue running , example: duplicate keys in database

    - Error(40):      Failure in a function that leads to that function not being able to complete.

    - Warn(30):       Failure in the Program that needs to alert the user but not halt , example: connection failed to DB, retry possible

    - Success(25):    Log succesful larger operations.

    - Info(20):       General Purpose logs, "Start importing file xy , finished importing file xy" and so on.

    - Debug(10):      Expands to log more frequently than Info, also with the file open at the time of logging.

    - Trace(5):       Log EVERYTHING , what method is being called, what file is opened (...)
    
"""
import sys
from loguru import logger

def custom_format(record ):
    lvl = record["level"].no
    if lvl == 50:
        return "<b><fg #b22222>{time:YYYY-MM-DD HH:mm:ss.SSSZZ} | {level:^8} | Proc: {process:^8} | Thread: {thread: ^16} | Mod: {module:^8} | Func: {function:^20} | Line: {line:^4} | Message: {message}</></>\n"
    elif lvl == 40:
        return "<b><fg #F37676>{time:YYYY-MM-DD HH:mm:ss.SSSZZ} | {level:^8} | Proc: {process:^8} | Thread: {thread: ^16} | Mod: {module:^8} | Func: {function:^20} | Line: {line:^4} | Message: {message}</></>\n"
    elif lvl == 30:
        return "<fg #F37676>{time:YYYY-MM-DD HH:mm:ss.SSSZZ} | {level:^8} | Proc: {process:^8} | Thread: {thread: ^16} | Mod: {module:^8} | Func: {function:^20} | Line: {line:^4} | Message: {message}</>\n"
    elif lvl == 25:
        return "<green>{time:YYYY-MM-DD HH:mm:ss.SSSZZ} | {level:^8} | Line: {line:^4} | Message: {message}</>\n"
    elif lvl == 20:
        return "<white>{time:YYYY-MM-DD HH:mm:ss.SSSZZ} | {level:^8} | Line: {line:^4} | Message: {message}</>\n"
    elif lvl == 10:
        return "<fg #808080>{time:YYYY-MM-DD HH:mm:ss.SSSZZ} | {level:^8} | Mod: {module:^8} | Func: {function:^8} | Line: {line:^4} | Message: {message}</>\n"
    elif lvl == 5:
        return "<dim><fg #808080>{time:YYYY-MM-DD HH:mm:ss.SSSZZ} | {level:^8} | Proc: {process: ^8} | Thread: {thread: ^16} | Mod: {module: ^8} | Function: {function: ^20} | Line: {line:^4} | Message: {message}</></>\n"

def setup_logging(
    level: str = "INFO",
    log_dir: str | None = None,
    ) -> None:
    # Clear definition
    logger.remove()
    logger.add(sys.stderr , level=level, format= custom_format)
    logger.info("Set Loglevel to: " + level)
    if level == "TRACE" or level == "DEBUG":
        logger.critical("Crit Test")
        logger.error("Error test")
        logger.warning("Warning test")
        logger.success("Success test")
        logger.info("Info test")
        logger.debug("Debug test")
        logger.trace("Trace test")
