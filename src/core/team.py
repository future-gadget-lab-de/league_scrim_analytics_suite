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
    #TODO:
    #WIP Querying the DB for teams so we don't use a globals file + easy support for multi-team
    #query = queries.returnSelectQuery(teams, [TeamName, PlayerID])
    #conn_params = loadDatabaseConfig()
    #executeQuery(query, conn_params)
    condition = "playerid =" + str(pUuid)
    query = returnSelectQuery("teamident", ["teamname"], where_cond= condition)
    team = executeSelectQuery(query)
    return str(team)

