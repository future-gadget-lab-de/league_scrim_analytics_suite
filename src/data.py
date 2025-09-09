import os
import json
import requests

def mapLink(patch: str, dataRequested: str):
    """
    Generates an API Link for ddragon, by giving the type of data requested

    ----------
    Parameters
    ----------
        patch (str):         The LoL patch number, the data will be based on.
        dataRequested (str): Determines the dataBase, which the function will downstream.
                             Currently supported: "summoner", "perk", "champion", "item"
    ----------
    Return
    ----------
        link (str):          The link according to the wanted type of data
    ----------
    """
    link = 'https://ddragon.leagueoflegends.com/cdn/' + patch + '/data/en_US/'

    # dataRequested -> suffix
    suffixes = {
        'perk':     'runesReforged.json',
        'item':     'item.json',
        'champion': 'champion.json',
        'summoner': 'summoner.json'
    }

    link += suffixes[dataRequested]

    return link

def loadDatabase(patch: str, dataRequested: str):
    """
    Saves and loads the databases determined by dataRequested.
    ----------
    Parameters
    ----------
        patch (str):         The LoL patch number, the data will be based on.
        dataRequested (str): Determines the dataBase, which the function will downstream.
                             Currently supported: "summoner", "perk", "champion", "item"
    ----------
    Return
    ----------
        data_dict (dict):    The Dictionary, which has the wanted lol data
    ----------
    """
    data_file = f"src/dictionaries/{dataRequested}.json"

    if os.path.isfile(data_file):
        with open(data_file) as data:
            # print("read json")
            return json.load(data)
    else:
        data_url = mapLink(patch, dataRequested)
        data_response = requests.get(data_url)
        data_dict = data_response.json()

        os.makedirs(os.path.dirname(data_file), exist_ok=True)

        with open(data_file, 'w') as data:
            # print("dumped json")
            json.dump(data_dict, data)
        
        return data_dict