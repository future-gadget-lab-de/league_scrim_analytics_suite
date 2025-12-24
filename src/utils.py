import os
import pathlib
import json
import requests
from src.globals import k_teamname, k_roster
from src.map import mapId

def findFile(path: str):
    """
    Finds the first file in the folder given by path.
    ----------
    Parameters
    ----------
        path (str):               the relative path, to a folder
    ----------
    Return
    ----------
        matchfile (str):          relative path for the file
    ----------
    """
    
    filelist = []
    with os.scandir(path) as ents:
        for e in ents:
            if e.is_dir() or "invalid" in e.name:
                continue
            else:
                filelist.append(e.name)
    filename=filelist[0]
    matchfile = path + filename
    return matchfile

def playerTeamCheck(pUuid):
    """
    Uses a Players identifier to check if he's on a known Team.
    ----------
    Parameters
    ----------
        pUuid (int):         The Players unique identifier ID
    ----------
    Return
    ----------
        team (str):          Known teamname or "enemyteam" as placeholder- Currently only supports ${Team_Name}
    ----------
    """
    #TODO: WIP Querying the DB for teams so we don't use a globals file + easy support for multi-team
    #query = queries.returnSelectQuery(teams, [TeamName, PlayerID])
    #conn_params = loadDatabaseConfig()
    #executeQuery(query, conn_params)
    if pUuid in k_roster:
        team = k_teamname
    else:
        team = "Random" #Enemy nicht zwangsläufig korrekt, wenn wir Daten anderer Teams betrachten.
    return team

def genBanArr(bans):

    """
    Takes the ban dictionary exported from the match data and makes it into an array of championnames
    ----------
    Parameters
    ----------
        bans (dict):         Dictionary mapping the ban order and champ ID together
    ----------
    Return
    ----------
        banarr (arr):          Array of Champion bans in the order they were banned by the Team
    ----------
    """

    banarr  = []

    try:
        for i in range (0,5):
            cId     = bans[i]['championId']
            cName   = mapId(cId, 'champion')
            banarr.append(cName)
    except:
        print("ERROR: The bans aren't proper in the given matchfile.")
        exit(0)

    return banarr


def loadDatabaseConfig():
    """
    Reads the Database config file and builds a dictionary for use in mariadb connection
    ----------
    Return
    ----------
        config_dict (dict):         Database parameters as a dictionary.
    ----------
    """

    config = dict()
    config_by_line = readFileByLine("config/database.conf")    
    
    for line in config_by_line:
        setting = line.replace(" ", "").split("=")   # remove whitespace and split
        config[setting[0]] = setting[1]    # build dict 
    return config
    
def readFileByLine(relPathToFile) -> list[str]:
    """
    read a file as an array of string lines
    """
    try:    
        with open(relPathToFile) as file:
            lines = [line.rstrip() for line in file]  # remove \n
            return lines
    except:
        print("ERROR: fileread not successful")
        exit(1)

def moveFile(file, dest: str) -> None:
    """
    Moves a file, to the provided destination
    ----------
    Parameters
    ----------
        file:                   the file, which is to move
        dest (str):             the destination as a relative path (containing the new name)
    ----------
    """
    path_hierarchy = dest.split("/")
    rel_path_to_folder = dest.removesuffix(path_hierarchy[-1])
    
    if not os.path.isdir(rel_path_to_folder):
        pathlib.Path(rel_path_to_folder).mkdir(parents=True, exist_ok=True)

    os.rename(file, dest)


def list_relative_filepaths(path: str) -> list[str]:
    """
    Collects all files in a directory tree and returns their paths relative to the given base path.
    ----------
    Parameters
    ----------
        path (str):                 The base directory to scan (relative path only).
    ----------
    Return
    ----------
        filepaths (list[str]):      List of file paths relative to the provided base directory.
    ----------
    """
    if os.path.isabs(path):
        raise ValueError("Path must be relative")

    base_path = os.path.abspath(path)

    if not os.path.isdir(base_path):
        return []

    filepaths: list[str] = []
    for root, _, files in os.walk(base_path):
        for filename in files:
            absolute_path = os.path.join(root, filename)
            relative_path = os.path.relpath(absolute_path, start=base_path)
            filepaths.append(relative_path)

    return filepaths

def reloadjsonfiles(relPathToJson: str, linkToJson: str) -> dict:
    """loads (or reloads) a specified .json

    this method checks, if a json is existens and returns it. if it doesnt
    exist, it gets scraped.

    Parameters
    ----------
    relPathToJson : str
        relative path to the .json file, which is checked for
    linkToJson : str
        link to the corresponding online source
    
    Returns
    -------
    data_dict : dict
        the json, from one of the sources above
    """

    # check if the file is already dumped
    if os.path.isfile(relPathToJson):
        with open(relPathToJson) as data:
            # print("read json")
            return json.load(data)
    else:
        data_url = linkToJson
        data_response = requests.get(data_url)
        data_dict = data_response.json()

        os.makedirs(os.path.dirname(relPathToJson), exist_ok=True)

        with open(relPathToJson, 'w') as data:
            # print("dumped json")
            json.dump(data_dict, data)
        
        return data_dict
