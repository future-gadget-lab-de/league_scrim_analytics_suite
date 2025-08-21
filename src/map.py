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