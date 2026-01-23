"""api scraping for riot api"""
import datetime, time, math
import numpy as np
from loguru import logger
from src.core.config import config, Configs
from src.utils.io import readJsonFile, requestJsonFile

def getPUIDbySummAndTagline(summonername: str, tagline: str, devKEY = False) -> str:
    """loads the metadata of a league account by summ and tagline
    
    Parameters
    ----------
    summonername : str
        the summonername, which the puid bases of
    tagline : str
        the tagline aswell
    devKey : bool
        if true, releases the wait time of 1 second
        
    Returns
    -------
    puuid : str
        the puuid according to the account
        
    """

    # reading api key
    api_key = config.general_settings[Configs.MAIN]["API_key"]
    # scraping summonerdata
    if not devKEY:
        time.sleep(1)
    resource_link = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summonername}/{tagline}?api_key={api_key}"
    data_of_user = requestJsonFile(resource_link)

    return data_of_user["puuid"]

def getSummonerSample(rank: str, queue: str, division: str, page: int = 1, devKEY = False) -> list[dict]:
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
    page : int
        the amount of samples, downloaded
    devKey : bool
        if true, releases the wait time of 1 second

    """

    # reading apikey
    api_key = config.general_settings[Configs.MAIN]["API_key"]
    # scraping
    if not devKEY:
        time.sleep(1)
    resource_link = f"https://euw1.api.riotgames.com/lol/league-exp/v4/entries/{queue}/{rank}/{division}?page={page}&api_key={api_key}"
    data_of_user: list = requestJsonFile(resource_link)
    
    return data_of_user


def getGameIdsByPuuid(puuid: str, devKEY = False) -> list:
    """loads a list of match ids
    
    Parameters
    ----------
    puuid : str
        the puuid the last 100 matches will get from
    devKey : bool
        if true, releases the wait time of 1 second
        
    Returns
    -------
    matchdict : dict
        a dict of matchids
    
    """

    # reading apikey
    api_key = config.general_settings[Configs.MAIN]["API_key"]
    # scraping
    if not devKEY:
        time.sleep(1)
    start = 0
    count = 100
    resource_link = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start={start}&count={count}&api_key={api_key}"
    data_of_user: list = requestJsonFile(resource_link)

    return data_of_user
    
def getGameById(gameid: str, saveLocation: str, devKEY = False) -> tuple[dict]:
    """loads the matchdata of a gameid
    
    Parameters
    ----------
    gameid : str
        the gameid of the match, we load
    devKey : bool
        if true, releases the wait time of 1 second
    saveLocation : str
        the location of the saved matchfiles
        
    Returns
    -------
    matchdict : dict
        a dict of matchdata
    
    """

    # reading apikey
    api_key = config.general_settings[Configs.MAIN]["API_key"]
    # scraping
    if not devKEY:
        time.sleep(1)
    resource_link_static = f"https://europe.api.riotgames.com/lol/match/v5/matches/{gameid}?api_key={api_key}"
    resource_link_timeline = f"https://europe.api.riotgames.com/lol/match/v5/matches/{gameid}/timeline?api_key={api_key}"
    data_of_match: list = requestJsonFile(resource_link_static, f"{saveLocation}/matches/{gameid}_static.json")
    data_of_time: list = requestJsonFile(resource_link_timeline, f"{saveLocation}/timelines/{gameid}_time.json")

    return (data_of_match, data_of_time)

def getMaxPageNumber(rank: str, queue: str, division: str) -> int:
    """a binary search for the last filled page in the summoner sample request
    
    Parameters
    ----------
    rank : str
        the competetive rank in lol. Needs to be capslock, f.ex.: DIAMOND
    queue : str
        the queue in which the rank is aqquiered. Supports: RANKED_SOLO_5x5, RANKED_TFT, RANKED_FLEX_SR, RANKED_FLEX_TT (really?)
    division : str
        Accepts: I, II, III, IV

    Returns
    -------
    maxPage : int
        the maximum filled page

    """
    maxPage = 1

    while len(getSummonerSample(rank, queue, division, maxPage)) > 0:
        
        maxPage *= 2

    empty_side = maxPage
    full_side = 1
    maxPage = math.floor((maxPage + full_side) / 2)

    while True:

        length_of_list = len(getSummonerSample(rank, queue, division, maxPage))

        # if pivot empty, go left
        if length_of_list == 0:
            tmp = maxPage
            maxPage = math.floor((full_side + maxPage) / 2)
            empty_side = tmp

        #if pivot full, go right
        elif length_of_list > 0:
            tmp = maxPage
            maxPage = math.floor((maxPage + empty_side) / 2)
            full_side = tmp

        if (empty_side - full_side) <= 1:
            return full_side

def getEqualDistGameSamples(
        rank: str, 
        queue: str, 
        division: str, 
        maxPageNumber: int,
        samplesize: int = 10, 
        saveLocation: str = config.general_settings[Configs.MAIN]["metadata_directory"]
    ) -> None:

    """generates a sample of matchfiles, based on rank, queue and division

    Parameters
    ----------
    rank : str
        the competetive rank in lol. Needs to be capslock, f.ex.: DIAMOND
    queue : str
        the queue in which the rank is aqquiered. Supports: RANKED_SOLO_5x5, RANKED_TFT, RANKED_FLEX_SR, RANKED_FLEX_TT (really?)
    division : str
        Accepts: I, II, III, IV
    maxPageNumber : int
        the maximum pagenumber of this sample
    samplesize : int, optional
        the number of matches that gets streamed
    saveLocation : str, optional
        a custom location, where the data gets saved. standard is: "src/scraping"
    
    """
    
    pages_of_data = maxPageNumber
    player_per_page = 205
    last_games = 100

    sample_game = np.random.uniform(0, last_games, samplesize)
    sample_player = np.random.uniform(0, player_per_page, samplesize)
    sample_page = np.random.uniform(0, pages_of_data, samplesize)
    sample_list = list()

    for page, player, game in zip(*(sample_page, sample_player, sample_game)):
        page_index = math.floor(page + 1)
        player_index = math.floor(player)
        game_index = math.floor(game)

        try:
            puuid = getSummonerSample(rank, queue, division, page_index)[player_index]["puuid"]
        except: 
            player_index = math.floor(np.random.uniform(0, len(getSummonerSample(rank, queue, division, page_index))))
            puuid = getSummonerSample(rank, queue, division, page_index)[player_index]["puuid"]

        try:
            gameid = getGameIdsByPuuid(puuid)[game_index]
        except:
            games = getGameIdsByPuuid(puuid)
            cus_number_of_games = len(games)
            if cus_number_of_games == 0:
                continue

            game_index = math.floor(np.random.uniform(0, cus_number_of_games))
            gameid = getGameIdsByPuuid(puuid)[game_index]

        sample_list.append(getGameById(gameid, saveLocation))

    return sample_list

