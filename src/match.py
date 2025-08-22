from src.utils import findMatchFile
import json
import os
from datetime import datetime, timedelta
from src.map import mapId

def loadPlayerIdentities(data):
    identity_dict = {}
    for i in range (0,10):
        pIdenData   = data['participantIdentities'][i] 
        pId         = pIdenData['participantId']
        pName       = pIdenData['player']['gameName']
        identity_dict[pId] = pName
    return identity_dict


def loadMetadata(data):
    """GameID""" 
    gameid=data['gameId']

    """ Match Duration"""
    time=str(timedelta(seconds=int(data['gameDuration'])))

    """ Patch Version """
    patch=".".join(str(data['gameVersion']).split(".")[:2])
    
    """ Match date """
    trimmedstamp=int(str(data['gameCreation'])[:-3])
    date=datetime.fromtimestamp(trimmedstamp).strftime("%Y-%m-%d")

    return gameid,patch,date,time

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
    playerIdentities = loadPlayerIdentities(data)
    print(playerIdentities)

    for i in range (0,10):
        pData   = data['participants'][i]
        pID     = pData['participantId']
        champ   = mapId(pData['championId'],'15.16.1', "champion")
        summ1   = mapId(pData['spell1Id'],'15.16.1', "summoner")
        summ2   = mapId(pData['spell2Id'],'15.16.1', "summoner")
        
    playerdata=""
    return playerdata

            