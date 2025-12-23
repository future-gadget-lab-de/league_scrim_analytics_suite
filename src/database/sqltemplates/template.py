from src.utils import readFileByLine


def importSQLQueries(relPathtoFile: str) -> list[str]:
    """
    test

    imports each query of provided .sql file \n

    Args:
        relPathtoFile (str):    relative path to the .sql file
    
    Returns:
        queries (list):         a list of sql queries as strings
    
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

    return queries