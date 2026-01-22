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
    PLAYER_2:       list[str]   = ["info","participants", "challenges", "legendaryItemUsed"]
    PLAYER_3:       list[str]   = ["info","participants","perks", "styles", "selections"]
    # teamdata
    TEAM_1:         list[str]   = ["info","teams"]
    TEAM_2:         list[str]   = ["info","teams", "bans"]


tableTypeForMatchV5: dict[MatchV5Keys, str] = {
    MatchV5Keys.META:     GameTable.META,
    MatchV5Keys.PLAYER_1: GameTable.PLAYER,
    MatchV5Keys.PLAYER_2: GameTable.PLAYER,
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

needsMetaDataMatchV5: dict[MatchV5Keys, str] = {
    MatchV5Keys.PLAYER_1: "gameId",
    MatchV5Keys.TEAM_1:   "gameId"
}
"""the tables produced by these keys, need metadata, to be assignable

Matchv5keys.PLAYER_1 -> "gameId"
MatchV5Keys.TEAM_1   -> "gameId"

"""

needsAggMatchV5: dict[MatchV5Keys, list[str]] = {
    MatchV5Keys.PLAYER_2: ["info","participants","participantId"],
    MatchV5Keys.PLAYER_3: ["info","participants","participantId"],
    MatchV5Keys.TEAM_2:   ["info", "teams","teamId"]
}
"""The tables produced by this keys, need further aggregation into the right table format.

ClientKeys.TEAM2        -> ["teams","teamId"]
MatchV5Keys.PLAYER_2:   -> ["info","participants","participantId"],
MatchV5Keys.PLAYER_3:   -> ["info","participants","participantId"],

"""

