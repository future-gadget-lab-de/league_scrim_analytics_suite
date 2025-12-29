from src.log_config import setup_logging
import logging, os
logger = logging.getLogger(__name__)

from src.visuals.gui import runAdvancedFrontend
from src.core.ops import importMatchfileData
from src.config import enrollSettings
from src.args import initiliazeParser
from src.utils import getRelPath


if __name__ == "__main__":

    enrollSettings(".config")

    args = initiliazeParser().parse_args()

    if args.verbose:
        setup_logging(level = "DEBUG")
    else:
        setup_logging(level = "INFO")

    if args.matchfile is not None:
        importMatchfileData(args.matchfile)

    # the gui starts here
    if args.gui:
        runAdvancedFrontend()

