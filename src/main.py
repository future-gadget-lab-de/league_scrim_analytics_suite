"""the entrypoint of this project."""
import sys, os, platform
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from loguru import logger
import pandas as pd
from src.core.config import config, Configs
from src.core.io.mariadb import updateConnectionState, databaseSetup, getCreationQueries
from src.visuals.gui import runAdvancedFrontend
from src.core.analyse.plugin import ApplyTemplate
from src.core.macros import importPipeline, executeSQLFiles
from src.core.logs import setup_logging
from src.args import initiliazeParser


def main() -> None:
    """the entryfunction of the lsas project"""
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
        sys.exit(0)
    if args.config is not None:
        config.reconfigure()

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
        importPipeline(args.matchfile)

    if args.execute is not None:
        logger.info(executeSQLFiles(args.execute))

    # the gui starts here
    if args.gui:
        runAdvancedFrontend()

    if args.template_file is not None:
        ApplyTemplate(args.template_file)

    config.writeSettings()

if __name__ == "__main__":
    getCreationQueries()
    ds = pd.read_csv("saved/metadata_match.csv")
    cols = list(ds[ds.columns[ds.loc[2].eq("meta")]].iloc[0,:])
    print(cols)
    main()
    
