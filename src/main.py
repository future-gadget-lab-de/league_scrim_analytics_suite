import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.log_config import setup_logging
import logging
logger = logging.getLogger(__name__)

from src.visuals.gui import runAdvancedFrontend
from src.core.ops import importMatchfileData
from src.config import enrollSettings
from src.args import initiliazeParser
from src.utils import getRelPath
from src.config import locPath_c

if __name__ == "__main__":

    parser = initiliazeParser()
    args = parser.parse_args()
    
    if not len(sys.argv) > 1:
        parser.print_help()
        sys.exit(0)

    # logging
    print(args)
    if args.very_verbose:
        setup_logging(level ="TRACE")
    elif args.verbose:
        setup_logging(level = "DEBUG")
    else:
        setup_logging(level = "INFO")
    
    logger.trace("Set Log-Level")
    if not os.path.isfile(locPath_c):
        enrollSettings(".config")
        logger.info("Enrolled a fresh config folder. restart the Application.")
        sys.exit(0)
    if args.config is not None:
        enrollSettings(args.config)

    # import of matchfiles
    logger.trace("Starting Import Routine")
    if args.matchfile is not None:
        importMatchfileData(args.matchfile)
    logger.trace("Finished Import Routine")
    # the gui starts here
    if args.gui:
        runAdvancedFrontend()
        
