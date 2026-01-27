from loguru import logger
import sys, os
import pandas as pd
from src.core.apis.ddragon import loadIdDataSet, scrapeRecentPatch

mappables: list[str] = ["champion", "summoner", "item", "perk"]

def initializeMapper(dataRequested: str, patch: str | None = None) -> dict[str, str]:
    """
    Maps the given id, to the corresponding name ingame.

    Parameters
    ----------
    dataRequested : str 
        Determines the dataBase, which the function will downstream.
        Currently supported: "summoner", "perk", "champion", "item"
    patch : str, optional
        if an Argument is passed, the passed patchnumber will be used
        instead of the most recent

    Returns
    -------
    final_dict : dict[str, str]
        the mapper
    """
    logger.trace("Started mapId Function.")
    data_dict = loadIdDataSet(dataRequested, patch=patch)
    placeholderstring = "-"
    try:
        if dataRequested in ['champion', 'summoner']:
            data_dict = data_dict['data']
            final_dict = { data_dict[name]['key']: data_dict[name]['name'].replace("'","") \
                            for name in data_dict.keys() }
            if dataRequested == "champion":
                final_dict["-1"] = placeholderstring
                final_dict["-"] = placeholderstring

            return final_dict

        if dataRequested == 'item':
            Items_dict = data_dict['data']

            keys = list(Items_dict.keys())

            final_dict = {key: Items_dict[str(key)]['name'].replace("'","") for key in keys}
            final_dict["0"] = placeholderstring

            return final_dict

        if dataRequested == 'perk':
            #Precision (8000), Domination (8100),  Sorcery (8200), Inspiration (8300), Resolve (8400)
            perk_dict = {str(item["id"]): item["key"] for item in data_dict} 
            rune_dict = {str(rune["id"]): rune["key"] for item in data_dict \
                                                for slot in item["slots"] \
                                                for rune in slot["runes"]}

            final_dict = rune_dict | perk_dict
            final_dict["0"] = placeholderstring

            return final_dict

    except:
        logger.info("Data requested was not found in Group: champion, summoner, item, perk! Input was: " + dataRequested)
        return dict()

class IdMapper:
    """handles the mapping of ids in the league datasets
    
    Attributes
    ----------
    loadedpatches : set[str]
        the set of loaded patch metadata files for mapping
    map : dict[tuple[str, str], dict[str, str]]
        (typeOfId,patch) --> mapfunction
        
    addPatchIfMissing : function
        checks, if the maps for the passed patch are loaded, 
        and loads them if they are not present
    """
    def __init__(self, patch: str = scrapeRecentPatch()):

        self.loadedpatches = set(patch)

        self.map: dict[tuple[str, str], dict[str, str]] = {
            (req, patch): initializeMapper(req, patch) for req in mappables
        }

    def addPatchIfMissing(self, patch: str):
        logger.trace("Check for a patch in the map handler.")
        if patch in self.loadedpatches:
            return

        logger.debug("adding new maps, to the map handler.")
        for req in mappables:
            self.map[(req, patch)] = initializeMapper(req, patch)

        self.loadedpatches.add(patch)

    def mapItem(self, id: str, req: str, patch: str):
        return self.map[(req,patch)][id]


lsasmapper: IdMapper = IdMapper()
"""the global map function"""
