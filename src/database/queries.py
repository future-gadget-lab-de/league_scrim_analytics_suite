from src.match import loadMatchData

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
    query = "INSERT INTO " + table + " ("
    
    # construct the tuple, where we insert
    for key in data.keys():
        query += str(key) + ","
    query = query.removesuffix(",")
    
    query += ") VALUES "

    query += str(tuple(data.values()))

    query += ";"

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
    metadata, playerdata, blueteamdata, redteamdata, data_file = loadMatchData(relPathtoFile)

    queries = list()

    queries.append(returnInsertQuery("metadata",metadata))
    for playerdict in playerdata:
        queries.append(returnInsertQuery("playerdata",playerdict))
    queries.append(returnInsertQuery("teamdata",blueteamdata))
    queries.append(returnInsertQuery("teamdata",redteamdata))

    return queries

def returnSelectQuery(table: str, columns: list[str]) -> str:
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
    query = "SELECT" 

    for col in columns:
        query += str(col) + ","

    query = query.removesuffix(",")
    query += "FROM" + table + ";"
    return query

