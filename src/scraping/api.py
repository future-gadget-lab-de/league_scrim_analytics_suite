import os,sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import datetime
from src.utils import loadjsonfiles
from src.config import readSettings, settings_list_c
from loguru import logger

def getPUIDbySummAndTagline(summonername: str, tagline: str) -> str:
    # reading api key
    settings_lsas = readSettings(settings_list_c[0])
    api_key = settings_lsas["API_key"]
    # scraping summonerdata
    resource_link = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summonername}/{tagline}?api_key={api_key}"
    data_of_user = loadjsonfiles(f"src/scraping/dictionaries/player/{summonername}_{tagline}.json", resource_link)

    return data_of_user["puuid"]


getPUIDbySummAndTagline("Emperor", "AGS")