import  os
from src.utils import readSettingsFile, writeSettingsFile

locPath_c = ".internal/location.conf"
from loguru import logger

def enrollSettings(relPathToConf: str) -> None:
    """
    Enrolls settings files for the user

    relPathToConf : str
        the relative path to the config folder
    
    """
    logger.trace("Checking if path to Config is relative")

    if os.path.isabs(relPathToConf):
        error_msg ="Path must be relative"
        logger.error(error_msg)
        raise ValueError(error_msg)
    else:
        logger.trace("Check successful")

    settings_dict = {
        "location": {
            "lsas": (relPathToConf + "/lsas.conf"),
            "database": (relPathToConf + "/database.conf")
        },
        "lsas": {
            "config_directory": relPathToConf, 
            "old_patch_support":"0",
            "csv_directory": "data",
            "mariadb": "0",
            "API_key": ""
        },
        "database" : {
            "host": "",
            "user": "",
            "password": "",
            "port": "",
            "database": ""
        }
    }

    if os.path.isfile(locPath_c):
        locs = readSettingsFile(locPath_c)

        for key in locs.keys():
            if os.path.isfile(locs[key]):
                settings_dict[key] = readSettingsFile(locs[key])

    for key in settings_dict.keys():
        if str(key) == "location":
            writeSettingsFile(settings_dict[key], locPath_c)
            continue

        writeSettingsFile(settings_dict[key],settings_dict["location"][key])
