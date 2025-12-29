from src.log_config import setup_logging
import logging
logger = logging.getLogger(__name__)

from src.visuals.gui import runAdvancedFrontend
from src.core.ops import enrollSettings
from src.args import initiliazeParser


if __name__ == "__main__":

    enrollSettings(".config")

    args = initiliazeParser().parse_args()

    if args.verbose:
        setup_logging(level = "DEBUG")
    else:
        setup_logging(level = "INFO")

    # the gui starts here
    if args.gui:
        runAdvancedFrontend()

