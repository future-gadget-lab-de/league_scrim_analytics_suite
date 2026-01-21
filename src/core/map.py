from loguru import logger
from src.scraping.data import loadIdDataSet

def mapId(id: int, dataRequested: str, patch: str | None = None) -> str:
    """
    Maps the given id, to the corresponding name ingame.

    Parameters
    ----------
    id : int
        An integer, which identifies a specific name.
    dataRequested : str 
        Determines the dataBase, which the function will downstream.
        Currently supported: "summoner", "perk", "champion", "item"
    patch : str, optional
        if an Argument is passed, the passed patchnumber will be used
        instead of the most recent

    Returns
    -------
    name : str
        The name, which corresponds to the id. if the mapping process fails, it inserts
        "placeholder" instead.
    """
    logger.trace("Started mapId Function.")
    data_dict = loadIdDataSet(dataRequested, patch=patch)
    mapped_id = "placeholder"
    try:
        if dataRequested in ['champion', 'summoner']:
            data_dict = data_dict['data']

            for name in data_dict:
                if data_dict[name]['key'] == str(id):
                    mapped_id = data_dict[name]['name'].replace("'","") 

        if dataRequested == 'item':
            Items_dict = data_dict['data']
            if id == 0:
                mapped_id = "No Item"
            mapped_id = Items_dict[str(id)]['name'].replace("'","")

        if dataRequested == 'perk':
            #Precision (8000), Domination (8100),  Sorcery (8200), Inspiration (8300), Resolve (8400)
            perk_dict = {item["id"]: item["key"] for item in data_dict} 
            rune_dict = {rune["id"]: rune["key"] for item in data_dict \
                                                for slot in item["slots"] \
                                                for rune in slot["runes"]}

            if id in [8000, 8100, 8300 ,8200, 8400]:
                mapped_id = perk_dict[id]
            else: mapped_id = rune_dict[id]

        if mapped_id != "placeholder": 
            logger.trace("Mapped the id "+ str(id) + "to: " + mapped_id)
            return mapped_id 
    except:
        logger.info("Data requested was not found in Group: champion, summoner, item, perk! Input was: " + dataRequested)
        return mapped_id

