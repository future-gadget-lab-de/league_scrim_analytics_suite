"""
Log Level explanation

**Critical** (50)
    Errors where program cannot continue running (e.g., duplicate keys in database).

**Error** (40)
    Failure in a function that prevents it from completing.

**Warning** (30)
    Failure that should alert the user but does not halt the program (e.g., DB connection failed; retry possible).

**Success** (25)
    Successful larger operations.

**Info** (20)
    General purpose logs (e.g., “start importing file … / finished importing file …”).

**Debug** (10)
    More frequent than Info; include additional state (e.g., open file).

**Trace** (5)
    Log everything (calls, opened files, …).
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
