import os
import pathlib
from src.globals import k_teamname, k_roster, k_patch, k_matchdirectory
from src.map import mapId

def getMatchCount():
    """
    Gives the Number of files found in the matchfile directory
    ----------
    Return
    ----------
        matchcount (int):          amount of matchfiles
    ----------
    """

    DIR = 'gamefiles/matchdata'
    count = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    return count

def findFile(path: str = k_matchdirectory):
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

    if pUuid in k_roster:
        team = k_teamname
    else:
        team = "Enemyteam"
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
            cName   = mapId(cId, k_patch, 'champion')
            banarr.append(cName)
    except:
        print("ERROR: The bans aren't proper in the given matchfile.")
        exit(0)

    return banarr

def readDatabaseConfig():
    """
    Reads the Database config file and builds a dictionary for use in mariadb connection
    ----------
    Return
    ----------
        config_dict (dict):         Database parameters as a dictionary.
    ----------
    """

    config_dict = {}
    with open("config/database.conf") as file:
        lines = [line.rstrip() for line in file]        # remove \n
        for line in lines:
            line        = line.replace(" ", "")         # remove whitespace
            splitline   = line.split("=")               # split into key-value
            config_dict[splitline[0]] = splitline[1]    # build dict 
    return(config_dict)
      

def moveFileDone(file, gameid):
    """
    Moves the given file into the directory for imported files & renames it to its gameid for storing.
    ----------
    Parameters
    ----------
        file (str):             Filename with relativ path
        gameid (int):           Number that respresents a unique identifier to the Match
    -------
    """

    new_file_string = "gamefiles/matchdata/done/" + str(gameid)
    if not os.path.isdir("gamefiles/matchdata/done/"):
        pathlib.Path("gamefiles/matchdata/done/").mkdir(parents=True, exist_ok=True)
    os.rename(file, new_file_string)