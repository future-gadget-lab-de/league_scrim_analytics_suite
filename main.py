from src.log_config import setup_logging
import logging, os, sys
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
        sys.exit(1)

    # logging
    if args.verbose:
        setup_logging(level = "DEBUG")
    else:
        setup_logging(level = "INFO")

    if not os.path.isfile(locPath_c):
        enrollSettings(".config")
        logger.info("Enrolled a fresh config folder. restart the Application.")
        sys.exit(0)

    if args.config is not None:
        enrollSettings(args.config)

    # import of matchfiles
    if args.matchfile is not None:
        importMatchfileData(args.matchfile)

    # the gui starts here
    if args.gui:
        runAdvancedFrontend()
        
