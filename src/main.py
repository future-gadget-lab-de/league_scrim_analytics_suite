import logging, sys, os, platform
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.config import config
from src.database.mariadb.execution import updateConnectionState, executeSQLFiles, databaseSetup
from src.visuals.gui import runAdvancedFrontend
from src.visuals.plot.plugin import ApplyTemplate
from src.core.ops import importMatchfileData
from src.args import initiliazeParser
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

    if config.needsReconfigure:
        config.reconfigure()
        logger.info("Enrolled a fresh config folder. restart the Application.")
        sys.exit(0)
    if args.config is not None:
        logger.trace("Starting enrollSettings Function with user settings:" + str(args.config))
        config.reconfigure()
        logger.info("Changed Config settings to user specified.")

    # is a connection possible?
    updateConnectionState()
    databaseSetup()

    if args.status: 
        if config.volatile_settings["_connected"] == "1":
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

    if args.template_file is not None:
        ApplyTemplate(args.template_file)

    config.writeSettings()
