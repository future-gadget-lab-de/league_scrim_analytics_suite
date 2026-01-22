from enum import Enum
from src.core.meta import GameTable

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
