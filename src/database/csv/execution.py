"""this file contains code, that does I/O functionality between .csv files and DataFrames"""
import duckdb, os
import pandas as pd
from src.config import readSettings, settings_list_c
from src.database.csv.manipulation import listOfDictsToDF

def readCsvs() -> list[pd.DataFrame]:
    """reads the internal database .csv files
    
    Returns
    -------
    data : list[pd.Dataframe]
        contains a list of data, namely meta-, team- and playerdata
        
    """
    settings_lsas = readSettings(settings_list_c[0])

    csv_dir = settings_lsas["csv_directory"]

    meta_dir = csv_dir + "/metadata.csv"
    team_dir = csv_dir + "/teamdata.csv"
    player_dir = csv_dir + "/playerdata.csv"

    if not os.path.isfile(player_dir):
        return [pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]

    meta = pd.read_csv(meta_dir)
    team = pd.read_csv(team_dir)
    player = pd.read_csv(player_dir)

    return [meta, team, player]

def compareTables(old_table: pd.DataFrame, new_table: pd.DataFrame, key: str) -> pd.DataFrame:
    """This is a helper method, which drops rows from the new_table, if the rows are alreade present in the old one.
    
    Parameters
    ----------
    old_table : pd.DataFrame
        the old data
    new_table : pd.DataFrame
        the new data, which is compared to the old one

    Returns
    -------
    diff_table : pd.DataFrame
        the rows which are totally new, in a dataframe    

    """
    drop_list = list()

    for skey in old_table[key]:
        for i in range(len(new_table[key])):
            if skey == new_table.loc[i,key]:
                drop_list.append(i)

    new_table = new_table.drop(drop_list, axis=0)

    return new_table

def insertDataAsCsv(metadata: list[dict], teamdata: list[dict], playerdata: list[dict]) -> None:
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
    meta_dir = csv_dir + "/metadata.csv"
    team_dir = csv_dir + "/teamdata.csv"
    player_dir = csv_dir + "/playerdata.csv"

    meta = listOfDictsToDF(metadata)
    team = listOfDictsToDF(teamdata)
    player = listOfDictsToDF(playerdata)

    data_list = [meta, team, player]
    dir_list = [meta_dir, team_dir, player_dir]

    os.makedirs(os.path.dirname(csv_dir+"/"), exist_ok=True)

    for i in range(3):
        if os.path.isfile(dir_list[i]):
            old_data = pd.read_csv(dir_list[i])
            data_list[i] = compareTables(old_data, data_list[i], "gameid")
            if data_list[i].empty:
                data_list[i] = old_data
                continue
            
            # concat if needed
            data_list[i] = pd.concat([data_list[i], old_data], axis=0, ignore_index=True)

        # write csvs
        data_list[i].to_csv(dir_list[i])

def runSelectOnDfs(query: str, tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
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
        con.register(name, df)
    try:
        return con.execute(query).df()
    finally:
        con.close()

