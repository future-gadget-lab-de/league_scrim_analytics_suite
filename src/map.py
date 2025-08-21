import requests
#import jsonify

def toChampion(id: int, Championdata_url: str):
    dataOfChampions_response = requests.get(Championdata_url)
    dataOfChampions_dict = dataOfChampions_response.json()

    Champions_dict = dataOfChampions_dict['data']

    for cname in Champions_dict:
        if Champions_dict[cname]['key'] == str(id):
            return cname

    return ""

def toItem(id: int, Itemdata_url: str):
    dataOfItems_response = requests.get(Itemdata_url)
    dataOfItems_dict = dataOfItems_response.json()

    Items_dict = dataOfItems_dict['data']

    return Items_dict[str(id)]['name']


def toPerk(id: int, Perkdata_url: str):
    dataOfPerks_reponse = requests.get(Perkdata_url)
    dataOfPerks_dict = dataOfPerks_reponse.json()
    
    perk_dict = {item["id"]: item["key"] for item in dataOfPerks_dict} #Precision (8000), Domination (8100),  Sorcery (8200), Inspiration (8300), Resolve (8400
    rune_dict = {rune["id"]: rune["key"] for item in dataOfPerks_dict for slot in item["slots"] for rune in slot["runes"]}

    if id in [8000, 8100, 8300 ,8200, 8400]:
        return perk_dict[id]
    return rune_dict[id]
