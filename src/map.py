import requests
from src.data import loadDatabase

# (id, dataRequested) --> explicit_name of given id
def mapId(id: int, patch: str, dataRequested: str):
    """
    Maps the given id, to the corresponding name ingame.

    ----------
    Parameters
    ----------
        id (int):            An integer, which identifies a specific name.
        patch (str):         The LoL patch number, the data will be based on.
        dataRequested (str): Determines the dataBase, which the function will downstream.
                             Currently supported: "summoner", "perk", "champion", "item"
    ----------
    Return
    ----------
        name (str):          The name, which corresponds to the id
    ----------
    """
    data_dict = loadDatabase(patch, dataRequested)

    if dataRequested in ['champion', 'summoner']:
        data_dict = data_dict['data']

        for name in data_dict:
            if data_dict[name]['key'] == str(id):
                return data_dict[name]['name']

    if dataRequested == 'item':
        Items_dict = data_dict['data']

        return Items_dict[str(id)]['name']

    if dataRequested == 'perk':
        #Precision (8000), Domination (8100),  Sorcery (8200), Inspiration (8300), Resolve (8400)
        perk_dict = {item["id"]: item["key"] for item in data_dict} 
        rune_dict = {rune["id"]: rune["key"] for item in data_dict \
                                            for slot in item["slots"] \
                                            for rune in slot["runes"]}

        if id in [8000, 8100, 8300 ,8200, 8400]:
            return perk_dict[id]
        return rune_dict[id]

