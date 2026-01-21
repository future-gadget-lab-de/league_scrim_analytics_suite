from enum import Enum

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