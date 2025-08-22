from src.utils import findMatchFile
import json
import os
from datetime import datetime, timedelta


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
            print(metadata)

            