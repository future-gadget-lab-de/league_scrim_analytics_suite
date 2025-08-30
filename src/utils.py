import os
from src.globals import teamname, roster, patch
from src.map import mapId

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
    banarr  = []
    for i in range (0,5):
        cId     = bans[i]['championId']
        cName   = mapId(cId, patch, 'champion')
        banarr.append(cName)
    return banarr