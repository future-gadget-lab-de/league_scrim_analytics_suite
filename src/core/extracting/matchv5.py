from enum import Enum

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
