"""constants and structural data of this project"""

from enum import StrEnum, Enum

version_c = "0.0.1"

class GameTable(StrEnum):
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

