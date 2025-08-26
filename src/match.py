from src.utils import findMatchFile
import json
import os
from datetime import datetime, timedelta
from src.map import mapId

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
        idendity_dict (dict):   Dictionary of the participant ID mapping to the player name
    ----------
    """
    identity_dict = {}
    for i in range (0,10):
        pIdenData   = data['participantIdentities'][i] 
        pId         = pIdenData['participantId']
        pName       = pIdenData['player']['gameName']
        identity_dict[pId] = pName
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

    if os.path.isfile(data_file):
        with open(data_file) as f:
            raw = f.read()
            data=json.loads(raw)
            
            metadata = loadMetadata(data)
            #print(metadata)
            playerdata = loadPlayerData(data)

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
        player_name (str):      Ingame Name of the Player
        team (str):             Enemy / US
        champ (str):            Champion Played
        summ1-2 (str):          Summoner Spell in Slot 1/2
        item1-6 (str):          Item in Slot 1-6#
        cwards_placed(int):     Amount of Controlwards placed
        wards_placed(int):      Amount of green / blue wards placed
        wards_destroyed(int):   Amount of wards cleared
        creep_score(int):       Ingame metric
        own_jng_kill(int):      Number of own-side jungle mobs cleared
        ene_jng_kill(int):      Number of enemy-side jungle mobs cleared
        kills(int):             Ingame metric
        deaths(int):            Ingame metric
        assists(int):           Ingame metric
        damage_dealt(int):      Damage dealt to champions
    ----------
    """
    playerIdentities = loadPlayerIdentities(data)
    print(playerIdentities)

    for i in range (0,10):
        # Create helper Variables 
        pData   = data['participants'][i]
        pID     = pData['participantId']
        pStats  = pData['stats']
        # Extract Data from first level 
        champ   = mapId(pData['championId'],'15.16.1', "champion")
        summ1   = mapId(pData['spell1Id'],'15.16.1', "summoner")
        summ2   = mapId(pData['spell2Id'],'15.16.1', "summoner")
        # Extract Itemdata  
        item_dict = {}
        for i in range (0,7):
            itemnr="item"+str(i)
            item_dict[i] = mapId(pStats[itemnr],'15.16.1','item')
        print(item_dict)

        # Extract Rune Data

    playerdata=""
    return playerdata

            