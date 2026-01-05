import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.log_config import setup_logging
import logging
logger = logging.getLogger(__name__)

from src.database.execution import updateConnectionState
from src.visuals.gui import runAdvancedFrontend
from src.core.ops import importMatchfileData, executeSQLFiles
from src.config import enrollSettings
from src.args import initiliazeParser
from src.utils import getRelPath, readSettingsFile
from src.config import locPath_c

if __name__ == "__main__":

    parser = initiliazeParser()
    args = parser.parse_args()
    
    if not len(sys.argv) > 1:
        parser.print_help()
        sys.exit(0)

    # logging
    if args.very_verbose:
        setup_logging(level ="TRACE")
    elif args.verbose:
        setup_logging(level = "DEBUG")
    else:
        setup_logging(level = "INFO")
    
    logger.trace("Set Log-Level")
    if not os.path.isfile(locPath_c):
        enrollSettings("config")
        logger.info("Enrolled a fresh config folder. restart the Application.")
        sys.exit(0)
    if args.config is not None:
        enrollSettings(args.config)


    # is a connection possible?
    updateConnectionState()

    if args.status: 
        if updateConnectionState():
            logger.info("You can connect, to your MariaDB Server!")
        else:
            logger.info("You can't establish a connection with your current MariaDB Config. Adjust the database.conf!")

    # import of matchfiles
    if args.matchfile is not None:
        logger.trace("Starting Import Routine")
        importMatchfileData(args.matchfile)
        logger.trace("Finished Import Routine")

    if args.execute is not None:
        executeSQLFiles(args.execute)

    # the gui starts here
    if args.gui:
        runAdvancedFrontend()
        
