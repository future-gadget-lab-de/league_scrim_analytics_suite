import logging, os

from src.utils import readSettingsFile, writeSettingsFile

locPath_k = ".config/location.conf"

def enrollSettings(relPathToConf: str) -> None:
    """
    Enrolls settings files for the user

    relPathToConf : str
        the relative path to the config folder
    
    """

    settings_dict = {
        "location": {
            "lsas": (relPathToConf + "/lsas.conf"),
            "database": (relPathToConf + "/database.conf")
        },
        "lsas": {
            "config_directory": relPathToConf, 
            "csv_directory": "",
            "mariadb": "",
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

    if os.path.isfile(locPath_k):
        locs = readSettingsFile(locPath_k)

        for key in locs.keys():
            if os.path.isfile(locs[key]):
                settings_dict[key] = readSettingsFile(locs[key])

    for key in settings_dict.keys():

        if str(key) == "location":
            writeSettingsFile(settings_dict[key], locPath_k)
            continue

        writeSettingsFile(settings_dict[key],settings_dict["location"][key])
    