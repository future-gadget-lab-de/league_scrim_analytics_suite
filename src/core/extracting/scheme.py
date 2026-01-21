from src.core.extracting.client import ClientKeys
from src.core.extracting.matchv5 import MatchV5Keys

class GameData(StrEnum):
    """the three tablenames of this project 
    
    Attributes
    ----------
    META : str
        = "metadata"
    TEAM : str
        = "teamdata"
    PLAYER : str
        = "playerdata"

    """
    META = "metadata"
    TEAM = "teamdata"
    PLAYER = "playerdata"

class importPipeline(Enum):
    """possible pipelines, we use currently
    
    Attributes
    ----------
    CLIENT : ClientKeys
        the pipeline for the client dumped data
    MATCHV5 : MatchV5Keys
        the pipeline for the matchv5 gathered data
    
    """
    CLIENT  = ClientKeys
    MATCHV5 = MatchV5Keys


needsAgg: dict[MatchV5Keys | ClientKeys, list[str]] = {
    ClientKeys.TEAM_2:    ["teams","teamId"],
    MatchV5Keys.PLAYER_2: ["info","participants","participantId"],
    MatchV5Keys.PLAYER_3: ["info","participants","participantId"],
    MatchV5Keys.TEAM_2:   ["info", "teams","teamId"]
}
"""The tables produced by this keys, need further aggregation into the right table format.

ClientKeys.TEAM2        -> ["teams","teamId"]
MatchV5Keys.PLAYER_2:   -> ["info","participants","participantId"],
MatchV5Keys.PLAYER_3:   -> ["info","participants","participantId"],
MatchV5Keys.TEAM_2:     -> ["info", "teams","teamId"]

"""

tableType: dict[ClientKeys|MatchV5Keys, str] = {
    ClientKeys.META:      GameData.META,
    ClientKeys.PLAYER_1:  GameData.PLAYER,
    ClientKeys.PLAYER_2:  GameData.PLAYER,
    ClientKeys.TEAM_1:    GameData.TEAM,
    ClientKeys.TEAM_2:    GameData.TEAM,
    MatchV5Keys.META:     GameData.META,
    MatchV5Keys.PLAYER_1: GameData.PLAYER,
    MatchV5Keys.PLAYER_2: GameData.PLAYER,
    MatchV5Keys.PLAYER_3: GameData.PLAYER,
    MatchV5Keys.TEAM_1:   GameData.TEAM,
    MatchV5Keys.TEAM_2:   GameData.TEAM,
}
"""classification of each resulting table

    ClientKeys.META      -> GameData.META,
    ClientKeys.PLAYER_1  -> GameData.PLAYER,
    ClientKeys.PLAYER_2  -> GameData.PLAYER,
    ClientKeys.TEAM_1    -> GameData.TEAM,
    ClientKeys.TEAM_2    -> GameData.TEAM,
    MatchV5Keys.META:    -> GameData.META,
    MatchV5Keys.PLAYER_1 -> GameData.PLAYER,
    MatchV5Keys.PLAYER_2 -> GameData.PLAYER,
    MatchV5Keys.PLAYER_3 -> GameData.PLAYER,
    MatchV5Keys.TEAM_1   -> GameData.TEAM,
    MatchV5Keys.TEAM_2   -> GameData.TEAM,

"""


def classify(member: ClientKeys | MatchV5Keys) -> GameData:
    return tableType[member]
