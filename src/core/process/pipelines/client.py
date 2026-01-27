"""Client pipeline."""
from enum import Enum
from src.core.meta import GameTable, gameTableLength
from src.core.process.map import lsasmapper
from src.core.team import playerTeamCheck
from loguru import logger
import pandas as pd

labellistclient = ["gameid", "date"]

class ClientKeys(Enum):
    """current paths to data, for pandas json_normalize
    
    Attributes
    ----------
    META : None
        the metadata is located in the root of the json, therefore there is nothing to pass
    PLAYER_1 : str
        root path for playerdata, therefore no agg needed
    PLAYER_2 : str
        the root path for playerdata meta stats, so no agg
    TEAM_1 : str
        the root path for teamdata, so no agg
    TEAM_2 : list[str]
        the path for bans in playerdata.
    
    """

    # metadata
    META:           None        = None
    # playerdata
    PLAYER_1:       str         = "participants"
    PLAYER_2:       str         = "participantIdentities"
    # teamdata
    TEAM_1:         str         = "teams"
    TEAM_2:         list[str]   = ["teams", "bans"]


tableTypeForClient: dict[ClientKeys, str] = {
    ClientKeys.META:      GameTable.META,
    ClientKeys.PLAYER_1:  GameTable.PLAYER,
    ClientKeys.PLAYER_2:  GameTable.PLAYER,
    ClientKeys.TEAM_1:    GameTable.TEAM,
    ClientKeys.TEAM_2:    GameTable.TEAM,
}
"""classification of each resulting table

    ClientKeys.META      -> GameTable.META,
    ClientKeys.PLAYER_1  -> GameTable.PLAYER,
    ClientKeys.PLAYER_2  -> GameTable.PLAYER,
    ClientKeys.TEAM_1    -> GameTable.TEAM,
    ClientKeys.TEAM_2    -> GameTable.TEAM,

"""
needsMetaDataClient: dict[ClientKeys, list[str]] = {
    ClientKeys.PLAYER_1: "gameId",
    ClientKeys.TEAM_1: "gameId"
}

"""the tables produced by these keys, need metadata, to be assignable

ClientKeys.PLAYER_1 -> "gameId"
ClientKeys.TEAM_1   -> "gameId"

"""

needsAggClient: dict[ClientKeys, list[str]] = { ClientKeys.TEAM_2: ["teams","teamId"] }
"""The tables produced by this keys, need further aggregation into the right table format.

MatchV5Keys.TEAM_2:     -> ["info", "teams","teamId"]

"""

subTestSet: set[str] = {'championId_0', 'championId_1', 'championId_2', 'championId_3', 'championId_4'}
"""a set of names to test if contained in the resulting table"""


mappables: dict[GameTable, dict[str, list[str]]] = {
    GameTable.META: {},
    GameTable.PLAYER: {
        "summoner": [
            "spell1Id",
            "spell2Id",
        ],
        "perk": [
            "stats_perk0",
            "stats_perk1",
            "stats_perk2",
            "stats_perk3",
            "stats_perk4",
            "stats_perk5",
        ],
        "item": [
            "stats_item0",
            "stats_item1",
            "stats_item2",
            "stats_item3",
            "stats_item4",
            "stats_item5",
            "stats_item6",
        ],
        "champion": [
            "championId"
        ]
    },
    GameTable.TEAM: {
        "champion": [
            "championId_0",
            "championId_1",
            "championId_2",
            "championId_3",
            "championId_4"
        ]
    }
}
