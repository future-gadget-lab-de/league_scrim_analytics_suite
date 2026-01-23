"""
This file contains a class for handling the current configuration of the program
"""
from loguru import logger
from enum import StrEnum
from src.utils.io import readSettingsFile, writeSettingsFile
from src.core.meta import version_c

locPathInt_c: str = ".internal/location.conf"
"""location for the **internal** config file"""

locPathSet_c: str = "config"
"""location for **general** settings"""

class Configs(StrEnum):
    """all configs, currently supported
    
    Attributes
    ----------
    MAIN : str
        the main settings of lsas
    DB : str
        the mariadb connection settings
        
    """
    MAIN = "lsas"
    DB = "mariadb"

template_c: dict[Configs, dict[str, str]] = {
    Configs.MAIN: {
        "old_patch_support":"0",
        "csv_directory": "data",
        "metadata_directory": "meta",
        "mariadb": "0",
        "API_key": "",
        "import_label": "gameid",
        "V5": "0"
    },
    Configs.DB: {
        "host": "",
        "user": "",
        "password": "",
        "port": "",
        "database": ""
    }
}
"""the template for config files in lsas"""

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

        self.general_settings: dict[Configs, dict[str, str]] = {
            Configs.MAIN: readSettingsFile(self.internal_settings[Configs.MAIN.value]),
            Configs.DB: readSettingsFile(self.internal_settings[Configs.DB.value])
        }

        if not self.general_settings:
            self.general_settings = template_c
            self.writeSettings()

        logger.trace("Initialized a fesh ConfigHandler.")


    def reconfigure(self):
        self.createInternals()
        self.writeInternals()

        for conf in Configs:
            keys = set(self.general_settings[conf].keys())
            temp_keys = set(template_c[conf].keys())
            keys_miss = temp_keys.difference(keys)

            for key in keys_miss:
                self.general_settings[conf][key] = template_c[conf][key]
        self.writeSettings()

        logger.debug("reconfigured the current configs configuration.")

    def createInternals(self):
        for conf in Configs:
            self.internal_settings[conf.value] = locPathSet_c + "/" + conf.value + ".conf"
        self.internal_settings["last_noticed_version"] = version_c

    def writeSettings(self):
        for config in Configs:
            writeSettingsFile(self.general_settings[config], self.internal_settings[config.value])
        logger.trace("changes in general settings written to file.")

    def writeInternals(self):
        writeSettingsFile(self.internal_settings, locPathInt_c)
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
