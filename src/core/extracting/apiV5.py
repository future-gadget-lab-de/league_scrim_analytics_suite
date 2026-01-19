
import json, os
from datetime import datetime, timedelta
from src.core.map import mapId
from src.core.team import playerTeamCheck
from src.config import readSettings, settings_list_c
from loguru import logger

def loadV5MatchData(relPath: str):
    """
    Wrapper method for the full data extraction of the first file found. V5
    
    Parameters
    ----------
    relPath : str
        The datafile for a given Match
    useIncludedGameversion : bool
        when true, the patch bundled with the gamefile is used for internal methods
    
    Returns
    -------
    metadata : dict       
        Dictionary which maps all features to their values
    playerdata : list[dict]
        Dictionary which maps all features to their values
    blueteamdata : dict
        Dictionary which maps all features to their values
    redteamdata : dict
        Dictionary which maps all features to their values
    """
    
    settings_lsas = readSettings(settings_list_c[0])

    if os.path.isfile(relPath):
        with open(relPath, encoding="utf-8") as f:
            raw                             = f.read()
            data_dict                       = json.loads(raw)

    patch = None

    if data_dict["info"]["endOfGameResult"] != "GameComplete":
        return dict(), dict(), dict(), dict()

    if settings_lsas["old_patch_support"] == "1":
        raw_version = data_dict["info"]["gameVersion"]
        raw_version_list = raw_version.split(".")
        patch = ".".join([raw_version_list[0],raw_version_list[1],"1"])

    metadata                        = loadMetadata(data_dict)
    playerdata                      = loadPlayerData(data_dict, patch)
    blueteamdata, redteamdata       = loadTeamData(data_dict, patch)

    return metadata, playerdata, blueteamdata, redteamdata

def loadMetadata(data) -> dict:
    """
    Extracts the GameID, Patchversion, duration and date of a given Match 
    
    Parameters
    ----------
    data : dict
        The datafile for a given Match
    
    Returns
    -------
    metadata : dict
        a dict containing the games metadata

    """
    metadata = dict()

    trimmedstamp=int(str(data['info']['gameCreation'])[:-3])
    
    metadata["date"    ] = datetime.fromtimestamp(trimmedstamp).strftime("%Y-%m-%d")
    metadata["gameid"  ] = data['info']['gameId']
    metadata["patch"   ] = ".".join(str(data['info']['gameVersion']).split(".")[:2])
    metadata["duration"] = str(timedelta(seconds=int(data['info']['gameDuration'])))

    return metadata

def loadTeamData(data: dict, patch: str | None = None) -> dict:
    """
    Extracts Playerdata from a given match 

    Parameters
    ----------
    data : dict            
        The datafile for a given Match

    Returns
    -------
    teamdata_blue : dict      
        Dict for blue team data
    teamdata_red : dict      
        Dict for red team data

    """

    # Create helper variable
    tlData      = data["info"]['teams'] 

    for i in range(2):

        teamdata = dict()
        tData   = tlData[i]

        # generating ban array
        banarr  = list()
        bans = tData['bans']
        try:
            for j in range (0,5):
                if len(bans)==0:
                    banarr.append("placeholder")
                    continue
                cId     = bans[j]['championId']
                if cId == -1:
                    banarr.append("placeholder")
                    continue
                cName   = mapId(cId, 'champion', patch)
                banarr.append(cName)
        except:
            logger.error("ERROR: The bans aren't proper in the given matchfile.")
            raise ValueError("die bans sind shit")
        bans = banarr

        for j in range(5):
            teamdata["ban"+str(j+1)] = bans[j]
        
        teamdata["gameid"] = data['info']['gameId']
        teamdata["teamid"] = tData['teamId']

        obj = tData["objectives"]
        teamdata["barons" ] = obj["baron"]["kills"]
        teamdata["firstbr"] = obj["baron"]["first"]
        teamdata["dragons"] = obj["dragon"]["kills"]
        teamdata["firstdr"] = obj["dragon"]["first"]
        teamdata["herald" ] = obj["riftHerald"]["kills"]
        teamdata["grubs"  ] = obj["horde"]["kills"]
        teamdata["firstbl"] = obj["champion"]["first"]
        # Yes riot actually fucked this up... # not TODO: not here
        teamdata["firstto"] = obj["tower"]["first"]
        teamdata["win"] = tData["win"]

        if i == 0:
            teamdata_red = teamdata
        else:
            teamdata_blue = teamdata
        
    
    return teamdata_blue, teamdata_red


def loadPlayerData(data: dict, patch: str | None = None) -> list[dict]:
    """
    Extracts Playerdata from a given match 

    Parameters
    ----------
    data : dict          
        The datafile for a given Match
    
    Returns
    -------
    player_dictlist : list[dict] 
        list, that has a data_dict for each player

    """
    
    # neue ausgabe als dict
    dict_list = list()

    for i in range(0,10):

        player_dict = dict()
        player_dict["gameid"] = data['info']['gameId']

        #helper
        pData   = data["info"]['participants'][i]
        # pID     = pData['participantId']
        # pStats  = pData['stats']
        
        player_dict["playerid"]         = str(player_dict["gameid"])+"_"+str(i)
        player_dict["teamid"]           = pData['teamId']
        player_dict["cwards_bought"]    = pData['visionWardsBoughtInGame']
        player_dict["wards_placed"]     = pData['wardsPlaced']
        player_dict["wards_destroyed"]  = pData['wardsKilled']
        player_dict["vision_score"]     = pData['visionScore']
        player_dict["minions_killed"]   = pData['totalMinionsKilled']
        player_dict["own_jng_kill"]     = pData['totalAllyJungleMinionsKilled']
        player_dict["ene_jng_kill"]     = pData['totalEnemyJungleMinionsKilled']
        player_dict["kills"]            = pData['kills']
        player_dict["deaths"]           = pData['deaths']
        player_dict["assists"]          = pData['assists']
        player_dict["damage_dealt"]     = pData['totalDamageDealtToChampions']
        player_dict["gold_earned"]      = pData['goldEarned']
        player_dict["turret_dmg"]       = pData['damageDealtToTurrets']
        player_dict["team"]             = "placeholder" # TODO: change: playerTeamCheck(playerIdentities[pID][1])
        player_dict["champ"]            = mapId(pData['championId'], "champion", patch)
        player_dict["summ1"]            = mapId(pData['summoner1Id'], "summoner", patch)
        player_dict["summ2"]            = mapId(pData['summoner2Id'], "summoner", patch)

        for j in range(7):
            itemnr="item"+str(j)
            player_dict["item"+str(j+1)] = mapId(pData[itemnr],'item', patch)
        for j in range(4):
            player_dict["rune"+str(j+1)] = mapId(pData["perks"]["styles"][0]["selections"][j]["perk"], 'perk', patch)

        player_dict["rune"+str(5)] = mapId(pData["perks"]["styles"][1]["selections"][0]["perk"], 'perk', patch)
        player_dict["rune"+str(6)] = mapId(pData["perks"]["styles"][1]["selections"][1]["perk"], 'perk', patch)
        dict_list.append(player_dict)

    return dict_list

            