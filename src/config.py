"""
This file contains multiple functionalities

"""
import  os
from src.utils import readSettingsFile, writeSettingsFile
from loguru import logger


locPath_c: str = ".internal/location.conf"
"""location for the **internal** config file"""

template_dict_c: dict[str] = {
    "lsas": {
        "old_patch_support":"0",
        "csv_directory": "data",
        "mariadb": "0",
        "API_key": "",
        "import_label": "gameid"
    },
    "mariadb": {
        "host": "",
        "user": "",
        "password": "",
        "port": "",
        "database": ""
    }
}
"""the template for config files in lsas"""


def enrollSettings(relPathToConf: str = "config")  -> list[str]:
    """
    Enrolls settings files for the user and uses the "settings_dict" as a template

    Parameters
    ----------
    relPathToConf : str, optional
        the relative path to the config folder

    Returns
    -------
    settings_list : list[str]
        returns a list of all settings (non internal)
    
    """
    logger.trace("Checking if path to Config is relative")
    if os.path.isabs(relPathToConf):
        error_msg: str ="Path must be relative"
        logger.error(error_msg)
        raise ValueError(error_msg)
    else:
        logger.trace("Check successful")

    # init variables
    settings_dict: dict[str] = template_dict_c
    internal_dict: dict[str] = dict()
    # writing hidden features, if not already present
    internal_dict["_connected"] = "0"
    settings_key_list: list[str] = list()

    # if the config directory has changed
    if os.path.isfile(locPath_c):
        internal_dict = readInternalSettings()
        # copy the current lsas configs
        for key in settings_dict.keys():
            settings_dict[key] = readSettings(str(key))

    # setup the internal dict
    for key in settings_dict.keys():
        # write file location into internal dict
        internal_dict[key] = relPathToConf + "/" + str(key) + ".conf"

    # write the internal .conf
    writeInternalSettings(internal_dict)

    # write all the other configs
    for key in settings_dict.keys():
        writeSettings(str(key), settings_dict[key])


def readInternalSettings() -> dict[str]:
    """returns the internal config file as a dict
    
    Returns
    -------
    internal_settings : dict[str]
        the internal settings in dict format
    
    """
    return readSettingsFile(locPath_c)

def writeInternalSettings(new_internals: dict[str]) -> None:
    """writes to the internal config file
    
    Parameters
    ----------
    new_internals : dict[str]
        the new settings to be written
        
    """
    writeSettingsFile(new_internals, locPath_c)

def readSettings(mode: str) -> dict[str]:
    """returns the data of a config file, given by mode
    
    Parameters
    ----------
    mode : str
        a string, which describes the name of the wanted .conf file
        
    Returns
    -------
    settings : dict[str]
        the settings wanted
        
    """
    internals = readInternalSettings()
    settings_loc = internals[mode]
    return readSettingsFile(settings_loc)

def writeSettings(mode: str, new_settings: dict[str]) -> None:
    """writes data to a config file, specified by mode
    
    Parameters
    ----------
    mode : str
        a string, which describes the name of the wanted .conf file
    new_settings : dict[str]
        the data, which will get written into the file
        
    """
    internals = readInternalSettings()
    settings_loc = internals[mode]
    writeSettingsFile(new_settings, settings_loc)

def initSettingsList() -> list[str]:
    if os.path.isfile(locPath_c):
        internal_dict = readInternalSettings()
        settings_list = list[str]()
        for key in internal_dict:
            # excluding hidden settings
            if not str(key).startswith("_"):
                settings_list.append(str(key))
        return settings_list
    else:
        return None

settings_list_c: list[str] = initSettingsList()
"""list, containing the settings 'keys'. 

'0'
    lsas    - the standard settings
'1'
    mariadb - the mariadb database settings

"""
