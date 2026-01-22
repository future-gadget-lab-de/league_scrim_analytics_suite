from src.database.queries import returnSelectQuery
from src.database.wrapper import executeSelectQuery
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
