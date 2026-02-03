"""
This file contains a class for handling the current configuration of the program
"""
import os
import pandas as pd
from loguru import logger
from enum import StrEnum
from src.utils.io import readSettingsFile, writeSettingsFile
from src.utils.path import transformPathtoFileList
from src.core.meta import version_c

locPathInt_c: str = ".internal/"
"""location for the **internal** config file"""

locPathSet_c: str = "config/"
"""location for **general** settings"""

class Configs(StrEnum):
    MAIN = "lsas"
    DB = "connections"
    PROF = "profiles"


templates: dict[Configs, dict[str, str]] = {
    Configs.MAIN: {
        "current_prof": "placeholder",
        "csv_directory": "data",
        "metadata_directory": "meta",
        "API_key": "",
        "import_label": "gameid",
    },
    Configs.DB: {
        "host": "",
        "port": "",
        "user": "",
        "password": "",
        "database": "",
    },
    Configs.PROF: {
        "mode": "csv",
        "con": "",
        "format": "client",
        "meta": "",
        "team": "",
        "player": "",
        "frame": "",
        "event": ""
    }
}

class ConfigHandler:
    """general handler for configs. This file loads an instance of this.

    Attributes
    ----------
    volatile_settings : dict[str,str]
        settings, which aren't written to files and load on runtime.
    internal_settings : dict[str,str]
        internal settings, which determine the filepath for general settings
    general_settings : dict[Configs, dict[str, str]]
        all general settings combined into one dict. 

    needsReconfigure : property
        returns if the settings need to be reconfigured
    reconfigure : function
        reconfigures all settings according to the blueprints in this file
    createInternals : function
        blueprint function for internal settings
    writeSettings : function
        writes current settings to file
    writeInternals : function
        writes the current internal settings to file
    
    """
    def __init__(self):

        self.volatile_settings: dict[str, str] = {
            "_connected": "0"
        }


        self.internal_settings: dict[str, str] = readSettingsFile(locPathInt_c)
        """rtfesafes"""
        
        if not self.internal_settings:
            self.createInternals()
            self.writeInternals()

        self.general_settings: dict[Configs, dict[str, str]] = {}

        self.general_settings[Configs.MAIN] = readSettingsFile(locPathSet_c + "lsas.conf")

        if not self.general_settings[Configs.MAIN]:
            self.general_settings[Configs.MAIN] = templates[Configs.MAIN]
            self.writeSettings()

        cur_prof =  self.general_settings[Configs.MAIN]["current_prof"]

        self.setProfile(cur_prof)

        logger.trace("Initialized a fresh ConfigHandler.")


    def reconfigure(self):

        self.createInternals()
        self.writeInternals()

        keys = set(self.general_settings[Configs.MAIN].keys())
        temp_keys = set(templates[Configs.MAIN].keys())
        keys_miss = temp_keys.difference(keys)

        for key in keys_miss:
            self.general_settings[Configs.MAIN][key] = templates[Configs.MAIN][key]
        self.writeSettings()

        logger.debug("reconfigured the current configs configuration.")

    def createInternals(self):
        self.internal_settings["last_noticed_version"] = version_c

    def createPlaceholder(self):
        mariadb_path = locPathSet_c + "connections/placeholder.conf"
        profile_path = locPathSet_c + "profiles/placeholder.conf"
        os.makedirs(os.path.dirname(mariadb_path), exist_ok=True)
        os.makedirs(os.path.dirname(profile_path), exist_ok=True)
        writeSettingsFile(templates[Configs.PROF], profile_path)



    def setProfile(self, name: str = "placeholder"):

        prof = locPathSet_c + "profiles/" + name + ".conf"
        self.general_settings[Configs.PROF] = readSettingsFile(prof)
        if not self.general_settings[Configs.PROF]:
            self.createPlaceholder()
            self.general_settings[Configs.MAIN]["current_prof"] = "placeholder"
            self.writeSettings()
            self.general_settings[Configs.PROF] = templates[Configs.PROF]
            self.general_settings[Configs.DB] = {}
            return
        self.general_settings[Configs.MAIN]["current_prof"] = name
        con_name = self.general_settings[Configs.PROF]["con"]
        if not con_name:
            self.general_settings[Configs.DB] = {}
            return
        con = locPathSet_c + "connections/" + con_name + ".conf"
        self.general_settings[Configs.DB] = readSettingsFile(con)

    def getFiles(self, config: Configs):
        listofFiles = transformPathtoFileList(locPathSet_c + config.value)
        result: list[str] = []
        for file in listofFiles:
            result.append(file.split("/")[-1].split(".")[0])
        return result


    def writeSettings(self):
        filepath = locPathSet_c + Configs.MAIN.value + ".conf"
        writeSettingsFile(self.general_settings[Configs.MAIN], filepath)
        logger.trace("changes in general settings written to file.")

    def writeInternals(self):
        writeSettingsFile(self.internal_settings, locPathInt_c + "location.conf")
        logger.trace("changes in internal settings written to file.")

    @property
    def needsReconfigure(self) -> bool:
        if not "last_noticed_version" in list(self.internal_settings.keys()):
            logger.debug("The version number is updated. configuration needs reconfiguring.")
            return True
        if self.internal_settings["last_noticed_version"] != version_c:
            logger.debug("No Version Number. configuration needs reconfiguring.")
            return True
        return False

config: ConfigHandler = ConfigHandler()
"""the config instance, used by the whole project."""
