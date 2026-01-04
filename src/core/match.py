import logging
logger = logging.getLogger(__name__)

import json, os
from datetime import datetime, timedelta

from src.core.map import mapId
from src.core.team import playerTeamCheck

from src.utils import findFile


def loadMatchData(relPath: str):
    """
    Wrapper method for the full data extraction of the first file found.
    
    Parameters
    ----------
    relPath : str
        The datafile for a given Match
    
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
    
    if os.path.isfile(relPath):
        with open(relPath) as f:
            raw                             = f.read()
            data_dict                       = json.loads(raw)
            metadata                        = loadMetadata(data_dict)
            playerdata                      = loadPlayerData(data_dict)
            blueteamdata, redteamdata       = loadTeamData(data_dict)

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
    With the content:
        gameid : int          
            Number that respresents a unique identifier to the Match
        patch : str            
            The LoL patch number
        date : str             
            Date of the Match played in the format: yyyy-mm-dd
        duration : str
            Duration of the match in the format: hh:mm:ss

    """
    metadata = dict()

    metadata["gameid"  ] = data['gameId']
    metadata["patch"   ] = ".".join(str(data['gameVersion']).split(".")[:2])
    trimmedstamp=int(str(data['gameCreation'])[:-3])
    metadata["date"    ] = datetime.fromtimestamp(trimmedstamp).strftime("%Y-%m-%d")
    metadata["duration"] = str(timedelta(seconds=int(data['gameDuration'])))

    return metadata

def loadTeamData(data) -> dict:
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
    teamdata = dict()

    # Create helper variable
    tlData      = data['teams'] 

    for i in range(2):
        tData   = tlData[i]
        teamdata["gameid"] = data['gameId']
        teamdata["teamid"] = tData['teamId']

        # generating ban array
        banarr  = list()
        bans = tData['bans']
        try:
            for i in range (0,5):
                cId     = bans[i]['championId']
                cName   = mapId(cId, 'champion')
                banarr.append(cName)
        except:
            print("ERROR: The bans aren't proper in the given matchfile.")
            exit(1)
        bans = banarr

        for j in range(5):
            teamdata["ban"+str(j+1)] = bans[j]
        
        teamdata["barons" ] = tData['baronKills'     ]
        teamdata["dragons"] = tData['dragonKills'    ]
        teamdata["herald" ] = tData['riftHeraldKills']
        teamdata["grubs"  ] = tData['hordeKills'     ]
        teamdata["firstbl"] = tData['firstBlood'     ]
        # Yes riot actually fucked this up...
        teamdata["firstdr"] = tData['firstDargon'    ]
        teamdata["firstto"] = tData['firstTower'     ]
        teamdata["firstbr"] = tData['firstBaron'     ]
        if tData['win'] == "Win":
            teamdata["win"] = True
        else:
            teamdata["win"] = False
        
        if i == 0:
            teamdata_red = teamdata
        else:
            teamdata_blue = teamdata
        
        teamdata = dict()

            
    return teamdata_blue, teamdata_red

def loadPlayerIdentities(data):
    """
    Generates a dictionary of the players present in the Match and mapping their participant ID to their 
    ingame Name

    Parameters
    ----------
    data : dict           
        The datafile for a given Match

    Returns
    -------
    idendity_dict : dict  
        Dictionary of the participant ID mapping to the player name and player-unique-identifieder

    """
    identity_dict = {}
    for i in range (0,10):
        pIdenData           = data['participantIdentities'][i] 
        pId                 = pIdenData['participantId']
        pName               = pIdenData['player']['gameName']
        pUuid               = pIdenData['player']['puuid']
        identity_dict[pId]  = (pName,pUuid)
        
    return identity_dict


def loadPlayerData(data) -> list[dict]:
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
    

    identity_dict = {}
    for i in range (0,10):
        pIdenData           = data['participantIdentities'][i] 
        pId                 = pIdenData['participantId']
        pName               = pIdenData['player']['gameName']
        pUuid               = pIdenData['player']['puuid']
        identity_dict[pId]  = (pName,pUuid)

    playerIdentities    = identity_dict
    
    # neue ausgabe als dict
    dict_list = list()

    for i in range(0,10):

        player_dict = dict()
        player_dict["gameid"] = data["gameId"]

        #helper
        pData   = data['participants'][i]
        pID     = pData['participantId']
        pStats  = pData['stats']
        
        player_dict["playerid"] = playerIdentities[pID][0]
        player_dict["teamid"] = pData['teamId']
        player_dict["champ"] = mapId(pData['championId'], "champion")
        player_dict["summ1"] = mapId(pData['spell1Id'], "summoner")
        player_dict["summ2"] = mapId(pData['spell2Id'], "summoner")
        for j in range(7):
            itemnr="item"+str(j)
            player_dict["item"+str(j+1)] = mapId(pStats[itemnr],'item')
        for j in range(6):
            runenr = "perk"+str(j)
            player_dict["rune"+str(j+1)] = mapId(pStats[runenr], 'perk')
        player_dict["cwards_bought"] = pStats['visionWardsBoughtInGame']
        player_dict["wards_placed"] = pStats['wardsPlaced']
        player_dict["wards_destroyed"] = pStats['wardsKilled']
        player_dict["vision_score"] = pStats['visionScore']
        player_dict["minions_killed"] = pStats['totalMinionsKilled']
        player_dict["own_jng_kill"] = pStats['neutralMinionsKilledTeamJungle']
        player_dict["ene_jng_kill"] = pStats['neutralMinionsKilledEnemyJungle']
        player_dict["kills"] = pStats['kills']
        player_dict["deaths"] = pStats['deaths']
        player_dict["assists"] = pStats['assists']
        player_dict["damage_dealt"] = pStats['totalDamageDealtToChampions']
        player_dict["gold_earned"] = pStats['goldEarned']
        player_dict["turret_dmg"] = pStats['damageDealtToTurrets']
        player_dict["team"] = playerTeamCheck(playerIdentities[pID][1])

        dict_list.append(player_dict)

    return dict_list

            