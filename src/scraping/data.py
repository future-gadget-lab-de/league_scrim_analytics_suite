import logging
logger = logging.getLogger(__name__)

import datetime
from src.utils import reloadjsonfiles
#TODO: Rewrite Logging
def scrapeRecentPatch() -> str:
    """scrapes the recent patch

    The recent patch gets scraped. period

    Returns
    -------
    patch : str
        the recent patch number as a string
    
    """
    logger.trace("Started scrapeRecentPatch function.")

    link = "https://ddragon.leagueoflegends.com/realms/euw.json"
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    data_file_path = f"src/scraping/dictionaries/EUW_{date}.json"

    logger.debug("Reload of the recent Patchnumber.")
    data_dict = reloadjsonfiles(data_file_path, link)
    logger.trace("Finished scrapeRecentPatch function.")
    return data_dict["v"]

def returnScrapeLink(dataRequested: str, patch: str | None = None) -> str:
    """
    Generates an API Link for ddragon, by giving the type of data requested

    Parameters
    ----------
    dataRequested : str
        Determines the dataBase, which the function will downstream.
        Currently supported: "summoner", "perk", "champion", "item"
    patch : str
        optional argument - specifies a custom patch

    Returns
    -------
    link : str
        The link according to the wanted type of data
    """
    logger.trace("Started returnScrapeLink function for patch: " + patch)
    if patch is None:
        patch = scrapeRecentPatch()

    link = 'https://ddragon.leagueoflegends.com/cdn/' + patch + '/data/en_US/'
    logger.debug("Generated API Link.")
    # dataRequested -> suffix
    suffixes = {
        'perk':     'runesReforged.json',
        'item':     'item.json',
        'champion': 'champion.json',
        'summoner': 'summoner.json'
    }

    link += suffixes[dataRequested]
    logger.trace("Finished returnScrapeLink function with output: " + link)
    return link

def loadDatabase(dataRequested: str, patch: str | None = None) -> dict:
    """
    Saves and loads the databases determined by dataRequested.
    
    Parameters
    ----------
    dataRequested : str 
        Determines the dataBase, which the function will downstream.
        Currently supported: "summoner", "perk", "champion", "item",
    patch : str
        optional argument - specifies a patch

    Returns
    -------
    data_dict : dict
        The Dictionary, which has the wanted lol data
    """
    logger.trace("Started function loadDatabase with dataRequested: " + dataRequested + ", for patch: " + patch)
    if patch is None:
        patch = scrapeRecentPatch()
        
    data_file_path = f"src/scraping/dictionaries/{dataRequested}_{patch}.json"
    logging.debug("Reload of the %s data.",dataRequested)

    scrape_link = returnScrapeLink(dataRequested)
    data_output = reloadjsonfiles(data_file_path, scrape_link)
    logger.trace("Finished loadDatabase function with output: + " str(data_output) )
    return data_output

