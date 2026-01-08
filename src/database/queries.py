from src.core.match import loadMatchData
from loguru import logger
#TODO: Rewrite Logging
def returnInsertQuery(table: str, data: dict) -> str:
    """returns a INSERT query

    For a passed dict, this method constructs a INSERT query, where the keys function as the table heads and the values, ofc as the values.

    Parameters
    ----------
    table : str
        the name of the table
    data : dict
        the dict, which has all necessary data
    
    Returns
    -------
    query : str
        the final INSERT query
    """
    logger.trace("Started returnInsertQuery for table: " + table + ", with data: " + str(data) )
    query = "INSERT INTO " + table + " ("
    logger.info("Generating Insert Queries")
    # construct the tuple, where we insert
    for key in data.keys():
        query += str(key) + ","
    query = query.removesuffix(",")
    query += ") VALUES "
    query += str(tuple(data.values()))
    query += ";"
    logger.trace("Finished returnInsertQuery with query: " + query)
    return query

def returnMatchfileQuery(relPathtoFile: str)-> list[str]:
    """query for matchfile importing.

    Returns a list of queries, which can be used to import a passed matchfile

    Parameters
    ----------
    relPathtoFile : str
        the relative path to a matchfile

    Returns
    -------
    queries : list[str]
        a list of queries to import the given matchfile
    """
    logger.trace("Starting returnMatchfileQuery function for file: " + relPathtoFile)
    metadata, playerdata, blueteamdata, redteamdata = loadMatchData(relPathtoFile)

    queries = list()
    logger.info("Generating matchfile Query")
    queries.append(returnInsertQuery("metadata",metadata))
    for playerdict in playerdata:
        queries.append(returnInsertQuery("playerdata",playerdict))
    queries.append(returnInsertQuery("teamdata",blueteamdata))
    queries.append(returnInsertQuery("teamdata",redteamdata))

    logger.trace("Finished returnMatchfileQuery.")
    return queries

def returnSelectQuery(table: str, columns: list[str], where_cond: str | None = None) -> str:
    """generates a SELECT query

    this method generates a sql query for selecting the colums in table.

    Parameters
    ----------
    table : str
        the name of the table
    columns : list[str]
        the columns to select

    Returns
    -------
    query : str
        the wanted SELECT query
    """
    logger.trace("Starting returnSelectQuery for table: " + table +", with columns: " +str(columns) )
    query = "SELECT " 
    logger.info("Generating select query")
    for col in columns:
        logger.trace("Adding: "+ str(col))
        query += str(col) + ","

    query = query.removesuffix(",")
    query += " FROM " + table
    if where_cond is not None:
        query += " WHERE " + where_cond
    
    query += ";"

    logger.trace("Finished returnSelectQuery with query: " + query )
    return query

