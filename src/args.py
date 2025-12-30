import argparse

def initiliazeParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lsas",
        description="league statistics analytics suite"
    )
    log_group = parser.add_mutually_exclusive_group()
    log_group.add_argument("-vv", "--very-verbose", help="sets the loggign level to TRACE.",action="store_true")
    log_group.add_argument("-v", "--verbose", help="sets the logging level to DEBUG. standard is INFO.", action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--matchfile", type=str, help="imports the matchfiles passed into the arg via absolute path (folder & file support)")
    group.add_argument("-c", "--config", type=str, help="adjusts the config folder with a passed relative path")
    group.add_argument("-g", "--gui", help="runs the graphical user interface, shipped with lsas", action="store_true")
    

    return parser

