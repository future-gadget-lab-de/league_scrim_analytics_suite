import logging
logger = logging.getLogger(__name__)

from src.globals import k_teamname, k_roster

def playerTeamCheck(pUuid: int) -> str:
    """
    Uses a Players identifier to check if he's on a known Team.

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
    if pUuid in k_roster:
        team = k_teamname
    else:
        team = "Random" #Enemy nicht zwangsläufig korrekt, wenn wir Daten anderer Teams betrachten.
    return team

