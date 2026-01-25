
from src.core.config import config, Configs
from src.core.meta import GameTable
import pandas as pd

tags = ["meta", "time", "game", "user", "bools", "scores", "ability", "stats", "gold", "cs", "challenge", "pings"]

class LeagueDataManager:

    def __init__(self):

        self.metacl = pd.read_csv("saved/metadata_client.csv")
        self.metama = pd.read_csv("saved/metadata_match.csv")
        self.playercl = pd.read_csv("saved/playerdata_client.csv")
        self.playerma = pd.read_csv("saved/playerdata_match.csv")
        self.teamcl = pd.read_csv("saved/teamdata_client.csv")
        self.teamma = pd.read_csv("saved/teamdata_match.csv")

        profile = config.general_settings[Configs.PROF]

        self.mode = profile["format"]

        self.present = {
            GameTable.META: not profile["meta"].split(",")[0] == "",
            GameTable.TEAM: not profile["team"].split(",")[0] == "",
            GameTable.PLAYER: not profile["player"].split(",")[0] == ""
        }

        self.filter = {
            GameTable.META: [int(ind) for ind in profile["meta"].split(",")] if self.present[GameTable.META] else [],
            GameTable.TEAM: [int(ind) for ind in profile["team"].split(",")] if self.present[GameTable.TEAM] else [],
            GameTable.PLAYER: [int(ind) for ind in profile["player"].split(",")] if self.present[GameTable.PLAYER] else []
        }


