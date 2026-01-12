"""
The whole purpose of this File is, to initialize a parser for later use in the Entrypoint file "main.py".
"""
import argparse

def initiliazeParser() -> argparse.ArgumentParser:
    """
    Initializes the Argumentparser with a proper layout.

    Returns
    -------
    parser : argparse.Argumentparser
        The Parser, with all Arguments needed at program startup
    
    """

    # init the argparser
    parser = argparse.ArgumentParser(
        prog="lsas",
        description="league statistics analytics suite"
    )

    # exclusive group for debugging
    log_group = parser.add_mutually_exclusive_group()
    log_group.add_argument("-vv", "--very-verbose", help="sets the loggign level to TRACE.",                    action="store_true")
    log_group.add_argument("-v", "--verbose",       help="sets the logging level to DEBUG. standard is INFO.",  action="store_true")

    # exclusive group for program operations
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--status",    action="store_true",  help="returns the current mariaDB status")
    group.add_argument("-g", "--gui",       action="store_true",  help="runs the graphical user interface, shipped with lsas")
    group.add_argument("-c", "--config",    type=str,             help="adjusts the config folder with a passed relative path")
    group.add_argument("-e", "--execute",   type=str,             help="execute a .sql file on the connected MariaDB Server (folder & file support)")
    group.add_argument("-f", "--matchfile", type=str,             help="imports the matchfiles passed into the arg via absolute path (folder & file support)")
    group.add_argument('-p',"--template-file", type=str, help='executes the template according to the plugin support')

    return parser

