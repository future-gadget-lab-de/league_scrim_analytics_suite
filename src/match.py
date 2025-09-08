from src.utils import findMatchFile, genBanArr, playerTeamCheck
from src.map import mapId
from src.globals import patch
from datetime import datetime, timedelta
import json
import os

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
        pUuid               =  pIdenData['player']['puuid']
        identity_dict[pId]  = (pName,pUuid)
        
    return identity_dict


def loadMetadata(data):
    """
    Extracts the GameID, Patchversion, duration and date of a given Match 
    ----------
    Parameters
    ----------
        data (json):            The datafile for a given Match
    ----------
    Return
    ----------
        idendity_dict (dict):   Dictionary of the participant ID mapping to the player name
        gameid (int):           Number that respresents a unique identifier to the Match
        duration (str):         Duration of the match in the format: hh:mm:ss
        date (str):             Date of the Match played in the format: yyyy-mm-dd
    ----------
    """

    gameid=data['gameId']
    duration=str(timedelta(seconds=int(data['gameDuration'])))
    patch=".".join(str(data['gameVersion']).split(".")[:2])

    trimmedstamp=int(str(data['gameCreation'])[:-3])
    date=datetime.fromtimestamp(trimmedstamp).strftime("%Y-%m-%d")

    return gameid,patch,date,duration

def loadMatchData():
    data_file = findMatchFile()
    print("INFO: Loading the File: " + str(data_file))
    if os.path.isfile(data_file):
        with open(data_file) as f:
            raw                             = f.read()
            data                            = json.loads(raw)
            metadata                        = loadMetadata(data)
            playerdata                      = loadPlayerData(data)
            blueteamdata, redteamdata       = loadTeamData(data)
            return metadata, playerdata, blueteamdata, redteamdata, data_file

def loadTeamData(data):
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

    # Create helper variable
    tlData      = data['teams'] 
    # Get Bans
    bData       = []
    rData       = []
    for i in range (0,2):
        tData   = tlData[i]
        tmpbans = tData['bans']
        bans    = genBanArr(tmpbans)
        barons  = tData['baronKills']
        dragons = tData['dragonKills']
        teamId  = tData['teamId']
        herald  = tData['riftHeraldKills']
        grubs   = tData['hordeKills']
        firstbl = tData['firstBlood']
        firstdr = tData['firstDargon'] # Yes riot actually fucked this up...
        firstto = tData['firstTower']
        firstbr = tData['firstBaron']
        if tData['win'] == "Win":
            win = True
        else:
            win = False
            
        temparr = [bans, barons, dragons, teamId, herald, grubs, firstbl, firstdr, firstto, firstbr, win]

        if i == 0:
            bData   = temparr
        elif i == 1: 
            rData   = temparr
    return bData, rData




def loadPlayerData(data):
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
        champ   = mapId(pData['championId'],patch, "champion")
        summ1   = mapId(pData['spell1Id'],patch, "summoner")
        summ2   = mapId(pData['spell2Id'],patch, "summoner")
        if pData['teamId'] == 100:
            side = "Blueside"
        else:
            side = "Redside"
        team = playerTeamCheck(playerIdentities[pID][1])
        # Extract Itemdata  
        item_dict = {}
        for n in range (0,7):
            itemnr="item"+str(n)
            item_dict[n] = mapId(pStats[itemnr],patch,'item')
        
        # Extract Rune Data
        rune_dict = {}
        for m in range (0,6):
            runenr = "perk"+str(m)
            rune_dict[m] = mapId(pStats[runenr], patch, 'perk')
        
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
                        own_jng_kill, ene_jng_kill, kills, deaths, assists, damage_dealt, gold_earned, turret_dmg, side, team]

        pData_dict[i] = player_data
    return pData_dict

            