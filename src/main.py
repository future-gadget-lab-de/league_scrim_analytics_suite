import logging, sys, os, platform
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database.execution import updateConnectionState
from src.visuals.gui import runAdvancedFrontend
from src.core.ops import importMatchfileData, executeSQLFiles
from src.config import enrollSettings
from src.args import initiliazeParser
from src.utils import getRelPath, readSettingsFile
from src.config import locPath_c
from src.log_config import setup_logging
from loguru import logger
if __name__ == "__main__":

    if platform.system() == "Windows":
        sys.argv.append("-g")

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
        logger.info(executeSQLFiles(args.execute))

    # the gui starts here
    if args.gui:
        logger.info("Starting GUI")
        runAdvancedFrontend()
