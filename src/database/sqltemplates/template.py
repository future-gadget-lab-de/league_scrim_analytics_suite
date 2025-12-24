import logging
logger = logging.getLogger(__name__)

from src.utils import readFileByLine

def importSQLQueries(relPathtoFile: str) -> list[str]:
    """imports a .sql file.

    imports each query of a passed .sql file as a list of strings

    Parameters
    ----------
    relPathtoFile : str
        relative path to the .sql file
    
    Returns
    -------
    queries : list[str]
        a list of sql queries as strings
    
    """

    sql_lines = readFileByLine(relPathtoFile)
    queries = list()

    query = ""
    for line in sql_lines:
        # skip empty lines
        if line.strip() == "":
            continue
        # skip commented lines
        if line.startswith("-- "):
            continue
        
        query += line

        if line.endswith(";"):
            queries.append(query)
            query = ""

    logger.debug("loaded the file: %s", relPathtoFile)
    return queries