import argparse

def initiliazeParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lsas",
        description="league statistics analytics suite"
    )
    parser.add_argument("-g", "--gui", help="runs the graphical user interface, shipped with lsas", action="store_true")
    parser.add_argument("-v", "--verbose", help="sets the logging level to DEBUG. standard is INFO.", action="store_true")
    parser.add_argument("-f", "--matchfile", type=str, help="imports the matchfiles passed into the arg via absolute path (folder & file support)")
    parser.add_argument("-c", "--config", type=str, help="adjusts the config folder with a passed relative path")

    return parser

