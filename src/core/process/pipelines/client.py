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

translationClient: dict[GameTable, dict[str, str]] = {

    GameTable.META: {
        "gameId":           "gameid",
        "gameVersion":      "patch",
        "gameCreationDate": "date",
        "gameDuration":     "duration"
    },
    GameTable.TEAM: {
        "gameId":           "gameid",
        "teamId":           "teamid",
        "championId_0":     "ban1",
        "championId_1":     "ban2",
        "championId_2":     "ban3",
        "championId_3":     "ban4",
        "championId_4":     "ban5",
        "baronKills":       "barons",
        "dragonKills":      "dragons",
        "riftHeraldKills":  "herald",
        "hordeKills":       "grubs",
        "firstBlood":       "firstbl",
        "firstTower":       "firstto",
        "firstDargon":      "firstdr",
        "firstBaron":       "firstbr",
        "win":              "win"
    },
    GameTable.PLAYER: {
        "gameId":                                "gameid",
        "player_gameName":                       "playerid",
        "teamId":                                "teamid",
        "championId":                            "champ",
        "spell1Id":                              "summ1",
        "spell2Id":                              "summ2",
        "stats_item0":                           "item1",
        "stats_item1":                           "item2",
        "stats_item2":                           "item3",
        "stats_item3":                           "item4",
        "stats_item4":                           "item5",
        "stats_item5":                           "item6",
        "stats_item6":                           "item7",
        "stats_perk0":                           "rune1",
        "stats_perk1":                           "rune2",
        "stats_perk2":                           "rune3",
        "stats_perk3":                           "rune4",
        "stats_perk4":                           "rune5",
        "stats_perk5":                           "rune6",
        "stats_visionWardsBoughtInGame":         "cwards_bought",
        "stats_wardsPlaced":                     "wards_placed",
        "stats_wardsKilled":                     "wards_destroyed",
        "stats_visionScore":                     "vision_score",
        "stats_totalMinionsKilled":              "minions_killed",
        "stats_neutralMinionsKilled":            "own_jng_kill",
        "stats_neutralMinionsKilledEnemyJungle": "ene_jng_kill",
        "stats_kills":                           "kills",
        "stats_deaths":                          "deaths",
        "stats_assists":                         "assists",
        "stats_totalDamageDealtToChampions":     "damage_dealt",
        "stats_goldEarned":                      "gold_earned",
        "stats_damageDealtToTurrets":            "turret_dmg",
        "player_puuid":                          "team"
    }
}

def translateTablesForClient(rawTables: dict[GameTable, pd.DataFrame]) -> None:
    """adjusts the passed rawTables according to the translation dict
    
    Parameters
    ----------
    rawTables : dict[GameTable, pd.DataFrame]
        the raw table, we will adjust in this method
    pipe : ImportPipeline
        the pipeline we used in the extraction
        
    """
    logger.trace("Start translation process for the result dataframe.")
    translateDict: dict[str,str] = translationClient

    patch_list = rawTables[GameTable.META].loc[0,"gameVersion"].split(".")
    rawTables[GameTable.META].loc[0,"gameVersion"] = ".".join(patch_list[0:2]) + ".1"
    read_patch = rawTables[GameTable.META].loc[0,"gameVersion"]

    lsasmapper.addPatchIfMissing(read_patch)

    for tableType in GameTable:
        # translate into the old layout
        transTablecols = list(translateDict[tableType].keys())
        tablecols = set(rawTables[tableType].columns)
        # insert empty columns, for all missing ones
        if not subTestSet.issubset(tablecols):
            for lostEntry in subTestSet: 
                rawTables[tableType][lostEntry] = "-"
        
        rawTables[tableType] = rawTables[tableType][transTablecols]

        mappables_list = list(mappables[tableType].keys())

        for mapping in mappables_list:
            for feature in mappables[tableType][mapping]:
                rawTables[tableType][feature] = rawTables[tableType][feature].astype('str')
                for i in range(gameTableLength[tableType]):
                    rawTables[tableType].loc[i, feature] = lsasmapper.map[(mapping, read_patch)][rawTables[tableType].loc[i, feature]]


        rawTables[tableType] = rawTables[tableType].rename(translateDict[tableType], axis="columns")


        # aggregate further test 
        match tableType:

            case GameTable.META:
                rawTables[tableType].loc[0,"date"] = rawTables[tableType].loc[0,"date"][0:10]

            case GameTable.TEAM:
                for i in range(2):
                    rawTables[tableType].loc[i,"win"] = True if (rawTables[tableType].loc[i,"win"] == "Win") else False

            case GameTable.PLAYER:
                for i in range(10):
                    rawTables[tableType].loc[i,"team"] = playerTeamCheck(rawTables[tableType].loc[i,"team"])


