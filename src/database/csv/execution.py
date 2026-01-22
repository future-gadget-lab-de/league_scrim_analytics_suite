"""this file contains code, that does I/O functionality between .csv files and DataFrames"""
import duckdb, os
import pandas as pd
from src.core.structure import GameTable
from src.config import readSettings, settings_list_c

def readCsv(csvdir: str) -> pd.DataFrame:
    if not os.path.isfile(csvdir):
        return pd.DataFrame()
    
    return pd.read_csv(csvdir)


def readCsvData() -> dict[GameTable, pd.DataFrame]:
    """reads the internal database .csv files
    
    Returns
    -------
    data : list[pd.Dataframe]
        contains a list of data, namely meta-, team- and playerdata
        
    """
    settings_lsas = readSettings(settings_list_c[0])
    csv_dir = settings_lsas["csv_directory"]

    return {
        GameTable.META: readCsv(csv_dir + "/" + GameTable.META.value + ".csv"),
        GameTable.PLAYER: readCsv(csv_dir + "/" + GameTable.PLAYER.value + ".csv"),
        GameTable.TEAM: readCsv(csv_dir + "/" + GameTable.TEAM.value + ".csv")
    }


def insertDataAsCsv(tabledict: dict[GameTable, pd.DataFrame]) -> None:
    """A method, which adds the passed data to the .csv database
    
    Parameters
    ----------
    metadata : list[dict]
        the metadata of a game
    teamdata : list[dict]
        the red- and blueteamdata of a game
    playerdata : list[dict]
        the data of all ten players of a game
        
    """
    settings_lsas = readSettings(settings_list_c[0])
    csv_dir = settings_lsas["csv_directory"]
    oldTabledict = readCsvData()

    os.makedirs(os.path.dirname(csv_dir+"/"), exist_ok=True)

    for tabletype in GameTable:
        pd.concat(oldTabledict[tabletype], tabledict[tabletype]).drop_duplicates().to_csv(csv_dir + "/" + tabletype.value + ".csv")


def runSelectOnDfs(query: str, tables: dict[GameTable, pd.DataFrame]) -> pd.DataFrame:
    """a helper method, which makes pd.Dataframes compatible with SELECT queries
    
    Parameters
    ----------
    query : str
        a proper SELECT query
    tables : dict[str, pd.DataFrame]
        tables describes a dict, where the 'tablename' gets mapped to the dataframe
    
    Returns
    -------
    selected_frame : pd.DataFrame
        the return of the SELECT query
        
    """

    con = duckdb.connect()
    for name, df in tables.items():
        con.register(name.value, df)
    try:
        return con.execute(query).df()
    finally:
        con.close()

