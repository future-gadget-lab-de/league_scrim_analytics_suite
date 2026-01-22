"""
This file contains multiple functionalities

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

    def __init__(self):
        self.volatile_settings: dict[str, str] = {
            "_connected": "0"
        }

        self.internal_settings: dict[str, str] = readSettingsFile(locPathInt_c)
        """rtfesafes"""

        self.general_settings: dict[Configs, dict[str, str]] = {
            Configs.MAIN: readSettingsFile(self.internal_settings[Configs.MAIN.value]),
            Configs.DB: readSettingsFile(self.internal_settings[Configs.DB.value])
        }

        if not self.internal_settings:
            self.createInternals()
            self.writeInternals()
            
        if not self.general_settings:
            self.general_settings = template_c
            self.writeSettings()

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

    def createInternals(self):
        for conf in Configs:
            self.internal_settings[conf.value] = locPathSet_c + "/" + conf.value + ".conf"
        self.internal_settings["last_noticed_version"] = version_c

    def writeSettings(self):
        for config in Configs:
            writeSettingsFile(self.general_settings[config], self.internal_settings[config.value])

    def writeInternals(self):
        writeSettingsFile(self.internal_settings, locPathInt_c)

    @property
    def needsReconfigure(self) -> bool:
        if not "last_noticed_version" in list(self.internal_settings.keys()):
            return True
        if self.internal_settings["last_noticed_version"] != version_c:
            return True
        return False

config: ConfigHandler = ConfigHandler()
