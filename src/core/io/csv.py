"""this file contains code, that does I/O functionality between .csv files and DataFrames"""
import duckdb, os
import pandas as pd
from loguru import logger
from src.core.meta import GameTable
from src.core.config import config, Configs

def readCsv(csvdir: str) -> pd.DataFrame:
    if not os.path.isfile(csvdir):
        return pd.DataFrame()
    
    return pd.read_csv(csvdir)


def csvToData() -> dict[GameTable, pd.DataFrame]:
    """reads the internal database .csv files
    
    Returns
    -------
    data : list[pd.Dataframe]
        contains a list of data, namely meta-, team- and playerdata
        
    """
    logger.debug("reading the csv data.")
    csv_dir = config.general_settings[Configs.MAIN]["csv_directory"]
    csv_dir += "/" + config.general_settings[Configs.MAIN]["current_prof"]
    return {
        GameTable.META: readCsv(csv_dir + "/" + GameTable.META.value + ".csv"),
        GameTable.PLAYER: readCsv(csv_dir + "/" + GameTable.PLAYER.value + ".csv"),
        GameTable.TEAM: readCsv(csv_dir + "/" + GameTable.TEAM.value + ".csv")
    }


def DataToCsv(tabledict: dict[GameTable, pd.DataFrame]) -> None:
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
    csv_dir = config.general_settings[Configs.MAIN]["csv_directory"]
    csv_dir += "/" + config.general_settings[Configs.MAIN]["current_prof"]
    oldTabledict = csvToData()

    os.makedirs(os.path.dirname(csv_dir+"/"), exist_ok=True)

    for tabletype in GameTable:
        df = pd.concat([oldTabledict[tabletype], tabledict[tabletype]], ignore_index=True)
        df = df.drop_duplicates()
        df.to_csv(csv_dir + "/" + tabletype.value + ".csv", index=False)
    
    logger.debug("writing the csv data.")

def runSelectOnCsv(query: str, tables: dict[GameTable, pd.DataFrame]) -> pd.DataFrame:
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
    logger.debug("run a query on dataframes.")
    con = duckdb.connect()
    for name, df in tables.items():
        con.register(name.value, df)
    try:
        return con.execute(query).df()
    finally:
        con.close()

