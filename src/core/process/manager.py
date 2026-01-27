
from src.core.config import config, Configs
from src.core.meta import GameTable,TimeTable
import pandas as pd

tags = ["meta", "time", "game", "user", "bools", "scores", "ability", "stats", "gold", "cs", "challenge", "pings"]

class LeagueDataManager:

    def __init__(self):

        self.tables = {
            "client": {
                GameTable.META: pd.read_csv("assets/metadata_client.csv"),
                GameTable.TEAM: pd.read_csv("assets/teamdata_client.csv"),
                GameTable.PLAYER: pd.read_csv("assets/playerdata_client.csv"),
                TimeTable.FRAME: pd.DataFrame(),
                TimeTable.EVENT: pd.DataFrame(),
            },
            "matchv5": {
                GameTable.META: pd.read_csv("assets/metadata_match.csv"),
                GameTable.TEAM: pd.read_csv("assets/teamdata_match.csv"),
                GameTable.PLAYER: pd.read_csv("assets/playerdata_match.csv"),
                TimeTable.FRAME: pd.read_csv("assets/framedata_match.csv"),
                TimeTable.EVENT: pd.read_csv("assets/eventdata_match.csv")
            }
        }

        self.updateManager()


    def updateManager(self):

        profile = config.general_settings[Configs.PROF]
        self.mode = profile["format"]

        self.recent_tables = self.tables[self.mode]

        mode = self.mode

        self.present: dict = {
            GameTable.META: not profile["meta"].split(",")[0] == "",
            GameTable.TEAM: not profile["team"].split(",")[0] == "",
            GameTable.PLAYER: not profile["player"].split(",")[0] == "",
            TimeTable.FRAME: not profile["frame"].split(",")[0] == "",
            TimeTable.EVENT: not profile["event"].split(",")[0] == ""

        }
        self.filter: dict = {
            GameTable.META: [int(ind) for ind in profile["meta"].split(",")] if self.present[GameTable.META] else [],
            GameTable.TEAM: [int(ind) for ind in profile["team"].split(",")] if self.present[GameTable.TEAM] else [],
            GameTable.PLAYER: [int(ind) for ind in profile["player"].split(",")] if self.present[GameTable.PLAYER] else [],
            TimeTable.FRAME: [int(ind) for ind in profile["frame"].split(",")] if self.present[GameTable.TEAM] else [],
            TimeTable.EVENT: [int(ind) for ind in profile["event"].split(",")] if self.present[GameTable.TEAM] else []
        }

        self.tagmap: dict =  {
            GameTable.META: { tag: self.tables[mode][GameTable.META][self.tables[mode][GameTable.META].columns[self.tables[mode][GameTable.META].loc[2].eq(tag)]] for tag in tags},
            GameTable.TEAM: { tag: self.tables[mode][GameTable.TEAM][self.tables[mode][GameTable.TEAM].columns[self.tables[mode][GameTable.TEAM].loc[2].eq(tag)]] for tag in tags},
            GameTable.PLAYER: { tag: self.tables[mode][GameTable.PLAYER][self.tables[mode][GameTable.PLAYER].columns[self.tables[mode][GameTable.PLAYER].loc[2].eq(tag)]]for tag in tags}
        }

        self.namemap: dict = {
            GameTable.META: { self.tables[mode][GameTable.META].columns[i]: self.tables[mode][GameTable.META].iloc[0,i] for i in range(len(self.tables[mode][GameTable.META].columns)) },
            GameTable.TEAM: { self.tables[mode][GameTable.TEAM].columns[i]: self.tables[mode][GameTable.TEAM].iloc[0,i] for i in range(len(self.tables[mode][GameTable.TEAM].columns)) },
            GameTable.PLAYER: { self.tables[mode][GameTable.PLAYER].columns[i]: self.tables[mode][GameTable.PLAYER].iloc[0,i] for i in range(len(self.tables[mode][GameTable.PLAYER].columns)) }, 
            TimeTable.FRAME: { self.tables[mode][TimeTable.FRAME].columns[i]: self.tables[mode][TimeTable.FRAME].iloc[0,i] for i in range(len(self.tables[mode][TimeTable.FRAME].columns)) },    
            TimeTable.EVENT: { self.tables[mode][TimeTable.EVENT].columns[i]: self.tables[mode][TimeTable.EVENT].iloc[0,i] for i in range(len(self.tables[mode][TimeTable.EVENT].columns)) }               
        }
        
centralmanager: LeagueDataManager = LeagueDataManager()