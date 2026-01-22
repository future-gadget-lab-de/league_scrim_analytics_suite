
import datetime
from loguru import logger
from src.core.config import config, Configs
from src.utils.io import readJsonFile, requestJsonFile

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
    data_file_path = f"{config.general_settings[Configs.MAIN]["metadata_directory"]}/dictionaries/EUW_{date}.json"

    logger.debug("Scraping recent Patch.")
    data_dict = readJsonFile(data_file_path)
    if not data_dict:
        data_dict = requestJsonFile(link, data_file_path)
    patch = data_dict["v"]

    logger.trace("Finished scrapeRecentPatch function.")
    logger.success("Scraped patch: " + patch)

    return patch

def returnScrapeLink(dataRequested: str, patch: str | None = None) -> str:
    """
    Generates an API Link for ddragon, by giving the type of data requested

    Parameters
    ----------
    dataRequested : str
        Determines the data, which the function will pull.
        Currently supported: "summoner", "perk", "champion", "item"
    patch : str
        optional argument - specifies a custom patch

    Returns
    -------
    link : str
        The link according to the wanted type of data
    """
    logger.trace("Started returnScrapeLink function for patch: " + str(patch))
    if patch is None:
        logger.info("No patch specified, using latest.")
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

def loadIdDataSet(dataRequested: str, patch: str | None = None) -> dict:
    """
    Saves and loads the IDs for data related to league games.
    
    Parameters
    ----------
    dataRequested : str 
        Determines the dataSet, which the function will load.
        Currently supported: "summoner", "perk", "champion", "item",
    patch : str
        optional argument - specifies a patch

    Returns
    -------
    data_dict : dict
        The Dictionary, which has the wanted lol data
    """
    logger.trace("Started function loadIdDataSet with dataRequested: " + dataRequested + ", for patch: " + str(patch))

    if patch is None:
        logger.info("No patch specified, using latest.")
        patch = scrapeRecentPatch()

    data_file_path = f"{config.general_settings[Configs.MAIN]["metadata_directory"]}/dictionaries/{dataRequested}_{patch}.json"
    logger.debug("Reload of the data: " + dataRequested)

    data_output = readJsonFile(data_file_path)
    if not data_output:
        scrape_link = returnScrapeLink(dataRequested)
        data_output = requestJsonFile(scrape_link, data_file_path)
        
    logger.success("Loaded IdDataSet: " +dataRequested) 
    return data_output

