from src.utils import findFile, genBanArr, playerTeamCheck
from src.map import mapId
from src.globals import k_patch
from datetime import datetime, timedelta
import json
import os

def loadMatchData(relPath = None):
    """
    Wrapper method for the full data extraction of the first file found.
    ----------
    Parameters
    ----------
        data (json):            The datafile for a given Match
    ----------
    Return
    ----------
        bData(arr):       Array for blue team data
        rData(arr):       Array for red team data
    ----------
    """
    data_file = findFile("gamefiles/matchdata/")
    if relPath is not None:
        data_file = relPath
    print("INFO: Loading the File: " + str(data_file))
    if os.path.isfile(data_file):
        with open(data_file) as f:
            raw                             = f.read()
            data                            = json.loads(raw)
            metadata                        = loadMetadata(data)
            playerdata                      = loadPlayerData(data)
            blueteamdata, redteamdata       = loadTeamData(data)
            return metadata, playerdata, blueteamdata, redteamdata, data_file

def loadMetadata(data) -> dict:
    """
    Extracts the GameID, Patchversion, duration and date of a given Match 
    ----------
    Parameters
    ----------
        data (json):            The datafile for a given Match
    ----------
    Return
    ----------
        gameid (int):           Number that respresents a unique identifier to the Match
        patch (str):            The LoL patch number
        date (str):             Date of the Match played in the format: yyyy-mm-dd
        duration (str):         Duration of the match in the format: hh:mm:ss
    ----------
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
    ----------
    Parameters
    ----------
        data (json):            The datafile for a given Match
    ----------
    Return
    ----------
        bData(arr):       Array for blue team data
        rData(arr):       Array for red team data
    ----------
    """
    teamdata = dict()

    # Create helper variable
    tlData      = data['teams'] 

    for i in range(2):
        tData   = tlData[i]
        teamdata["gameid"] = data['gameId']
        teamdata["teamid"] = tData['teamId']

        bans    = genBanArr(tData['bans'])
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
    ----------
    Parameters
    ----------
        data (json):            The datafile for a given Match
    ----------
    Return
    ----------
        idendity_dict (dict):   Dictionary of the participant ID mapping to the player name and player-unique-identifieder
    ----------
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
    ----------
    Parameters
    ----------
        data (json):            The datafile for a given Match
    ----------
    Return
    ----------
        pData_dict(dict):       Dictionary that maps Number 0-9 to the Player and their data.
    ----------
    """
    
    playerIdentities    = loadPlayerIdentities(data)
    pData_dict          = {}

    for i in range (0,10):
        # Create helper Variables 
        pData   = data['participants'][i]
        pID     = pData['participantId']
        pStats  = pData['stats']

        # Extract Data from first level 
        champ   = mapId(pData['championId'],k_patch, "champion")
        summ1   = mapId(pData['spell1Id'],k_patch, "summoner")
        summ2   = mapId(pData['spell2Id'],k_patch, "summoner")
        teamid  = pData['teamId']
        team    = playerTeamCheck(playerIdentities[pID][1])
        # Extract Itemdata  
        item_dict = {}
        for n in range (0,7):
            itemnr="item"+str(n)
            item_dict[n] = mapId(pStats[itemnr],k_patch,'item')
        
        # Extract Rune Data
        rune_dict = {}
        for m in range (0,6):
            runenr = "perk"+str(m)
            rune_dict[m] = mapId(pStats[runenr], k_patch, 'perk')
        
        # Extract general Data
        cwards_bought   =   pStats['visionWardsBoughtInGame']
        wards_placed    =   pStats['wardsPlaced']
        wards_destroyed =   pStats['wardsKilled']
        vision_score    =   pStats['visionScore']
        minions_killed  =   pStats['totalMinionsKilled']
        own_jng_kill    =   pStats['neutralMinionsKilledTeamJungle']
        ene_jng_kill    =   pStats['neutralMinionsKilledEnemyJungle']
        kills           =   pStats['kills']
        deaths          =   pStats['deaths']
        assists         =   pStats['assists']
        damage_dealt    =   pStats['totalDamageDealtToChampions']
        gold_earned     =   pStats['goldEarned']
        turret_dmg      =   pStats['damageDealtToTurrets']
       
        player_data     = [playerIdentities[pID],champ, summ1, summ2, item_dict.values(), rune_dict.values(), \
                        cwards_bought, wards_placed, wards_destroyed, vision_score, minions_killed, \
                        own_jng_kill, ene_jng_kill, kills, deaths, assists, damage_dealt, gold_earned, turret_dmg, teamid, team]
        pData_dict[i] = player_data

    # neue ausgabe als dict
    player_dict = dict()
    dict_list = list()

    for i in range(0,10):
        player_dict["gameid"] = data["gameId"]
        player_dict["playerid"] = pData_dict[i][0][0]
        player_dict["teamid"] = pData_dict[i][19]
        player_dict["champ"] = pData_dict[i][1]
        player_dict["summ1"] = pData_dict[i][2]
        player_dict["summ2"] = pData_dict[i][3]
        for i in range(7):
            player_dict["item"+str(i+1)] = item_dict[i]
        for i in range(6):
            player_dict["rune"+str(i+1)] = rune_dict[i]
        player_dict["cwards_bought"] = pData_dict[i][6]
        player_dict["wards_placed"] = pData_dict[i][7]
        player_dict["wards_destroyed"] = pData_dict[i][8]
        player_dict["vision_score"] = pData_dict[i][9]
        player_dict["minions_killed"] = pData_dict[i][10]
        player_dict["own_jng_kill"] = pData_dict[i][11]
        player_dict["ene_jng_kill"] = pData_dict[i][12]
        player_dict["kills"] = pData_dict[i][13]
        player_dict["deaths"] = pData_dict[i][14]
        player_dict["assists"] = pData_dict[i][15]
        player_dict["damage_dealt"] = pData_dict[i][16]
        player_dict["gold_earned"] = pData_dict[i][17]
        player_dict["turret_dmg"] = pData_dict[i][18]
        player_dict["team"] = pData_dict[i][20]

        dict_list.append(player_dict)
        player_dict = dict()

    return dict_list

            