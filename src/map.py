import requests

def mapLink(patch: str, dataRequested: str):
    """
    Generates an API Link for ddragon, by giving the type of data requested

    ----------
    Parameters
    ----------
        patch (str):         The LoL patch number, the data will be based on.
        dataRequested (str): Determines the dataBase, which the function will go through.
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

# (id, dataRequested) --> explicit_name of given id
def mapId(id: int, patch: str, dataRequested: str):
    """
    Maps the given id, to the corresponding name ingame.

    ----------
    Parameters
    ----------
        id (int):            An integer, which identifies a specific name.
        patch (str):         The LoL patch number, the data will be based on.
        dataRequested (str): Determines the dataBase, which the function will go through.
                             Currently supported: "summoner", "perk", "champion", "item"
    ----------
    Return
    ----------
        name (str):          The name, which corresponds to the id
    ----------
    """
    data_url = mapLink(patch, dataRequested)
    data_response = requests.get(data_url)
    data_dict = data_response.json()

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

