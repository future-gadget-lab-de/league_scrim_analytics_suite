"""MatchV5 pipeline"""
from enum import Enum
from src.core.meta import GameTable

class MatchV5Keys(Enum):
    """current paths to data, for pandas json_normalize
    
    Attributes
    ----------
    META : None
        Since the metadata sits at the root, there is not path to pass
    PLAYER_1 : list[str]
        This keypath serves as the root of the playerdata, therefore 
        this does not need aggregation.
    PLAYER_2 : list[str]
        this keypath has the data of the use of legendary items
    PLAYER_3 : list[str]
        this keypath has the data of the perks, selected by the player
    TEAM_1 : list[str]
        this keypath serves as the root for teamdata, therefore this does not
        need further aggregation
    TEAM_2 : list[str]
        this keypath is for the data of bans
    """
    # metadata
    META:           None        = None
    # playerdata
    PLAYER_1:       list[str]   = ["info", "participants"]
    # PLAYER_2:       list[str]   = ["info","participants", "challenges", "legendaryItemUsed"]
    PLAYER_3:       list[str]   = ["info","participants","perks", "styles", "selections"]
    # teamdata
    TEAM_1:         list[str]   = ["info","teams"]
    TEAM_2:         list[str]   = ["info","teams", "bans"]


tableTypeForMatchV5: dict[MatchV5Keys, str] = {
    MatchV5Keys.META:     GameTable.META,
    MatchV5Keys.PLAYER_1: GameTable.PLAYER,
    # MatchV5Keys.PLAYER_2: GameTable.PLAYER,
    MatchV5Keys.PLAYER_3: GameTable.PLAYER,
    MatchV5Keys.TEAM_1:   GameTable.TEAM,
    MatchV5Keys.TEAM_2:   GameTable.TEAM,
}
"""classification of each resulting table

    MatchV5Keys.META:    -> GameTable.META,
    MatchV5Keys.PLAYER_1 -> GameTable.PLAYER,
    MatchV5Keys.PLAYER_2 -> GameTable.PLAYER,
    MatchV5Keys.PLAYER_3 -> GameTable.PLAYER,
    MatchV5Keys.TEAM_1   -> GameTable.TEAM,
    MatchV5Keys.TEAM_2   -> GameTable.TEAM,

"""

needsMetaDataMatchV5: dict[MatchV5Keys, list[str]] = {
    MatchV5Keys.PLAYER_1: ["info","gameId"],
    MatchV5Keys.TEAM_1:   ["info","gameId"]
}
"""the tables produced by these keys, need metadata, to be assignable

Matchv5keys.PLAYER_1 -> "gameId"
MatchV5Keys.TEAM_1   -> "gameId"

"""

needsAggMatchV5: dict[MatchV5Keys, list[str]] = {
    # MatchV5Keys.PLAYER_2: ["info","participants","participantId"],
    MatchV5Keys.PLAYER_3: ["info","participants","participantId"],
    MatchV5Keys.TEAM_2:   ["info", "teams","teamId"]
}
"""The tables produced by this keys, need further aggregation into the right table format.

ClientKeys.TEAM2        -> ["teams","teamId"]
MatchV5Keys.PLAYER_2:   -> ["info","participants","participantId"],
MatchV5Keys.PLAYER_3:   -> ["info","participants","participantId"],

"""
translationMatchV5: dict[GameTable, dict[str, str]] = {

    GameTable.META: {
        "info_gameId":           "gameid",
        "info_gameVersion":      "patch",
        "info_gameCreation":     "date",
        "info_gameDuration":     "duration"
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

