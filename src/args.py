import argparse

def initiliazeParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lsas",
        description="league statistics analytics suite"
    )
    parser.add_argument("-g", "--gui", help="runs the graphical user interface, shipped with lsas", action="store_true")
    parser.add_argument("-v", "--verbose", help="sets the logging level to DEBUG. standard is INFO.", action="store_true")
    return parser

