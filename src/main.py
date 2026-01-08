import logging, os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.visuals.gui import runAdvancedFrontend
from src.core.ops import importMatchfileData
from src.config import enrollSettings
from src.args import initiliazeParser
from src.utils import getRelPath
from src.config import locPath_c
from src.log_config import setup_logging
from loguru import logger
if __name__ == "__main__":

    parser = initiliazeParser()
    args = parser.parse_args()
    
    if not len(sys.argv) > 1:
        parser.print_help()
        sys.exit(0)

    # logging
    if args.very_verbose:
        level ="TRACE"
    elif args.verbose:
        level = "DEBUG"
    else:
        level = "INFO"

    setup_logging(level)

    if not os.path.isfile(locPath_c):
        enrollSettings("config")
        logger.info("Enrolled a fresh config folder. restart the Application.")
        sys.exit(0)
    if args.config is not None:
        logger.trace("Starting enrollSettings Function with user settings:" + str(args.config))
        enrollSettings(args.config)
        logger.info("Changed Config settings to user specified.")

    # import of matchfiles
    if args.matchfile is not None:
        importMatchfileData(args.matchfile)
    # the gui starts here
    if args.gui:
        logger.info("Starting GUI")
        runAdvancedFrontend()
