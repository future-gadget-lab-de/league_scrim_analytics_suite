import os
from src.globals import teamname, roster, patch
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

def findMatchFile():
    """
    Finds the first file in the gamefiles/matchdata folder.
    ----------
    Return
    ----------
        matchfile (str):          relative path for the matchfile
    ----------
    """
    
    filename = os.listdir("gamefiles/matchdata")[0]
    matchfile = "gamefiles/matchdata/"+filename
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

    if pUuid in roster:
        team = teamname
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

    for i in range (0,5):
        cId     = bans[i]['championId']
        cName   = mapId(cId, patch, 'champion')
        banarr.append(cName)

    return banarr

def readDatabaseConfig():
    config_dict = {}
    with open("config/database.conf") as file:
        lines = [line.rstrip() for line in file]        # remove \n
        for line in lines:
            line        = line.replace(" ", "")         # remove whitespace
            splitline   = line.split("=")               # split into key-value
            config_dict[splitline[0]] = splitline[1]    # build dict 
    return(config_dict)
      
