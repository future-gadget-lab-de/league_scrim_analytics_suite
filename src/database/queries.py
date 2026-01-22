"""this file contains code for generating .sql queries"""
from loguru import logger
import pandas as pd
from src.core.structure import GameTable

#TODO: Rewrite Logging HACK: little bit messy
def returnInsertQuery(table: GameTable, df: pd.DataFrame, ignoreDuplicateOn: str | None = None) -> str:
    """returns a INSERT query

    For a passed dict, this method constructs a INSERT query, where the keys function as the table heads and the values, ofc as the values.

    Parameters
    ----------
    table : GameTable
        the name of the table
    df : pd.DataFrame
        the dataframe, you want to get a query for
    deleteDuplicates : bool, optional
        this arg is very hacky, since it assumes the unique key, to be the gameid. ignores duplicate errors such
    
    Returns
    -------
    query : str
        the final INSERT query
    """
    logger.trace("Started returnInsertQuery for table: " + table.value + ", with data: " + str(df) )
    query = "INSERT INTO " + table.value 
    logger.info("Generating Insert Queries")
    # insertion
    query += " ("
    for colname in list(df.columns):
        query += str(colname)
        query += ", "
    query = query.removesuffix(", ")
    query += ")"
    # values
    query += " VALUES "
    rows, cols = df.shape
    for r in range(rows):
        query += "("
        for c in range(cols):
            if f"{df.iloc[r,c]}" == "True":
                query += f"'{1}'" + ", "
                continue
            if f"{df.iloc[r,c]}" == "False":
                query += f"'{0}'" + ", "
                continue
            query += f"'{df.iloc[r,c]}'" + ", "
        query = query.removesuffix(", ")
        query += "), "
    query = query.removesuffix(", ")
    if ignoreDuplicateOn is not None:
        query += f"ON DUPLICATE KEY UPDATE {ignoreDuplicateOn}={ignoreDuplicateOn}"
    query += ";"

    logger.trace("Finished returnInsertQuery with query: " + query)
    return query

def returnMatchfileQuery(tabledict: dict[GameTable, pd.DataFrame])-> list[str]:
    """query for matchfile importing.

    Returns a list of queries, which can be used to import a passed matchfile

    Parameters
    ----------
    tabledict : tabledict: dict[GameTable, pd.DataFrame]
        the result of the data extraction

    Returns
    -------
    queries : list[str]
        a list of queries to import the given matchfile
    """

    queries = list()
    for tabletype in GameTable:
        queries.append(returnInsertQuery(tabletype, tabledict[tabletype], ignoreDuplicateOn="gameid"))

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

