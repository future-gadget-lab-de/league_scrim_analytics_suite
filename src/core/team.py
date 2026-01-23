"""helperfile for assigning a team to a group of playerdata"""

from src.core.io.wrapper import executeSelectQuery
from src.utils.sqlquery import returnSelectQuery
from loguru import logger

def playerTeamCheck(pUuid: str) -> str:
    """
    Uses a Players identifier to check if he's on a known Team.
    This only works with scrim data , as the pUuid there and riots pUuid are not indentical.
    Parameters
    ----------
    pUuid : int         
        The Players unique identifier ID
    
    Returns
    -------
    team : str
        Known teamname or "enemyteam" as placeholder- Currently only supports ${Team_Name}
    """
    return "-" # FIX:
    logger.trace("Started playerTeamCheck function with input: " + pUuid)
    condition = "playerid='" + str(pUuid) + "'"
    query = returnSelectQuery("teamident", ["teamname"], where_cond= condition)
    team = executeSelectQuery(query)
    if team.empty:
        team = "randoms"
    else:
        team = str(team.iloc[0,0])
    logger.trace("Finished playerTeamCheck function with input: " + team)
    return team

