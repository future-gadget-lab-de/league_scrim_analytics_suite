import datetime
from src.utils import reloadjsonfiles

def scrapeRecentPatch() -> str:
    """scrapes the recent patch

    The recent patch gets scraped. period

    Returns
    -------
    patch : str
        the recent patch number as a string
    
    """

    link = "https://ddragon.leagueoflegends.com/realms/euw.json"
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    data_file_path = f"src/dictionaries/EUW_{date}.json"
    
    data_dict = reloadjsonfiles(data_file_path, link)

    return data_dict["v"]



def returnScrapeLink(dataRequested: str) -> str:
    """
    Generates an API Link for ddragon, by giving the type of data requested

    Parameters
    ----------
    dataRequested : str
        Determines the dataBase, which the function will downstream.
        Currently supported: "summoner", "perk", "champion", "item", "patch"

    Returns
    -------
    link : str
        The link according to the wanted type of data
    """
    patch = scrapeRecentPatch()
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

def loadDatabase(dataRequested: str) -> dict:
    """
    Saves and loads the databases determined by dataRequested.
    
    Parameters
    ----------
    dataRequested : str 
        Determines the dataBase, which the function will downstream.
        Currently supported: "summoner", "perk", "champion", "item", "patch"

    Returns
    -------
    data_dict : dict
        The Dictionary, which has the wanted lol data
    """
    patch = scrapeRecentPatch()
    data_file_path = f"src/dictionaries/{dataRequested}_{patch}.json"
    scrape_link = returnScrapeLink(dataRequested)

    return reloadjsonfiles(data_file_path, scrape_link)

