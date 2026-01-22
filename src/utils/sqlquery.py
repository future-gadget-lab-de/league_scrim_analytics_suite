"""this file contains code for generating .sql queries"""
from loguru import logger
from src.core.meta import GameTable
import pandas as pd

#TODO: Rewrite Logging HACK: little bit messy
def returnInsertQuery(table: str, df: pd.DataFrame, ignoreDuplicateOn: str | None = None) -> str:
    """returns a INSERT query

    For a passed dict, this method constructs a INSERT query, where the keys function as the table heads and the values, ofc as the values.

    Parameters
    ----------
    table : GameTable
        the name of the table
    df : pd.DataFrame
        the dataframe, you want to get a query for
    ignoreDuplicateOn : str, optional
        if passed, ignores duplicates on the passed key
    
    Returns
    -------
    query : str
        the final INSERT query
    """
    logger.trace("Started returnInsertQuery for table: " + table + ", with data: " + str(df) )
    query = "INSERT INTO " + table 
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

