import logging, os

from src.utils import readSettingsFile, writeSettingsFile

locPath_c = ".internal/location.conf"

def enrollSettings(relPathToConf: str) -> None:
    """
    Enrolls settings files for the user

    relPathToConf : str
        the relative path to the config folder
    
    """
    if os.path.isabs(relPathToConf):
        raise ValueError("Path must be relative")

    settings_dict = {
        "location": {
            "lsas": (relPathToConf + "/lsas.conf"),
            "database": (relPathToConf + "/database.conf"),
            "connected": "0"
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
    