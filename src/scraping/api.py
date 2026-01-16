import os,sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import datetime
from src.utils import loadjsonfiles
from src.config import readSettings, settings_list_c
from loguru import logger

def getPUIDbySummAndTagline(summonername: str, tagline: str) -> str:
    """loads the metadata of a league account by summ and tagline
    
    Parameters
    ----------
    summonername : str
        the summonername, which the puid bases of
    tagline : str
        the tagline aswell
        
    Returns
    -------
    puuid : str
        the puuid according to the account
        
    """

    # reading api key
    settings_lsas = readSettings(settings_list_c[0])
    api_key = settings_lsas["API_key"]
    # scraping summonerdata
    resource_link = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summonername}/{tagline}?api_key={api_key}"
    data_of_user = loadjsonfiles(f"src/scraping/dictionaries/player/{summonername}_{tagline}.json", resource_link)

    return data_of_user["puuid"]

def getSummonerSample(rank: str, queue: str, division: str, samplesize: int = 1) -> None:
    """
    loads a sample of players according to the passed arguments.

    Parameters
    ----------
    rank : str
        the competetive rank in lol. Needs to be capslock, f.ex.: DIAMOND
    queue : str
        the queue in which the rank is aqquiered. Supports: RANKED_SOLO_5x5, RANKED_TFT, RANKED_FLEX_SR, RANKED_FLEX_TT (really?)
    division : str
        Accepts: I, II, III, IV
    samplesize : int
        the amount of samples, downloaded

    """

    # reading apikey
    settings_lsas = readSettings(settings_list_c[0])
    api_key = settings_lsas["API_key"]
    # scraping
    for i in range(samplesize):
        resource_link = f"https://euw1.api.riotgames.com/lol/league-exp/v4/entries/{queue}/{rank}/{division}?page={i+1}&api_key={api_key}"
        data_of_user: list = loadjsonfiles(f"src/scraping/dictionaries/player/sample/{rank}_{queue}_{division}_{i+1}.json", resource_link)
        
        if not data_of_user:
            break

def getGameIdsByPuuid(puuid: str) -> dict:
    """loads a list of match ids
    
    Parameters
    ----------
    puuid : str
        the puuid the last 100 matches will get from
        
    Returns
    -------
    matchdict : dict
        a dict of matchids
    
    """

    # reading apikey
    settings_lsas = readSettings(settings_list_c[0])
    api_key = settings_lsas["API_key"]
    # scraping
    start = 0
    count = 100
    resource_link = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start={start}&count={count}&api_key={api_key}"
    data_of_user: list = loadjsonfiles(f"src/scraping/matches/{puuid}.json", resource_link)
    
def getGameById(gameid: str) -> tuple[dict]:
    """loads the matchdata of a gameid
    
    Parameters
    ----------
    gameid : str
        the gameid of the match, we load
        
    Returns
    -------
    matchdict : dict
        a dict of matchdata
    
    """

    # reading apikey
    settings_lsas = readSettings(settings_list_c[0])
    api_key = settings_lsas["API_key"]
    # scraping
    resource_link_static = f"https://europe.api.riotgames.com/lol/match/v5/matches/{gameid}?api_key={api_key}"
    resource_link_timeline = f"https://europe.api.riotgames.com/lol/match/v5/matches/{gameid}/timeline?api_key={api_key}"
    data_of_match: list = loadjsonfiles(f"src/scraping/matches/{gameid}_static.json", resource_link_static)
    data_of_time: list = loadjsonfiles(f"src/scraping/matches/{gameid}_time.json", resource_link_timeline)

    return (data_of_match, data_of_time)



getGameById("EUW1_7682915481")
#getSummonerSample("DIAMOND", "RANKED_SOLO_5x5", "IV", 3)
getPUIDbySummAndTagline("Emperor", "AGS")