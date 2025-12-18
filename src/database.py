import mariadb
import sys


def buildConnection(conn_params):
    """
    Uses connection parameters to build a connection and a cursor(interface with server) to a database host
    ----------
    Parameters
    ----------
        conn_params (dict):            Dicitonary containing connection data, read from /conf/database.conf
    ----------
    Return
    ----------
        conn    (connection):       Handles the connection to a MariaDB or MySQL database server. It encapsulates a database session.
        cur     (cursor):           Executes SQL statements and procedures, and manages fetching results.
    ----------
    """

    conn_params['port'] = int(conn_params['port']) 
    conn = mariadb.connect(**conn_params)
    cur = conn.cursor()
    return conn, cur

def insertData(data, conn_params, gameid, table: str):
    """
    Inserts data into a database & table based on the given parameters, main method to wrap the building and executing of query & conneciton
    ----------
    Parameters
    ----------
        data (array):               Array that contains all data to be inserted into the table
        conn_params (dict):         Dicitonary containing connection data, read from /conf/database.conf
        gameid (int):               Primary or part of the composite key for the Database tables
        table (str):                Name of the table, used for selecting the pattern to insert.
    ----------
    """

    # establish a connection
    conn, cur  = buildConnection(conn_params)
    # Build query
    #table = ["metadata","teamdata","playerdata"]
    #tableColums = []
    #for i in range(3):
    #    if not isTableCreated(table[i],cur, conn):
    #        createTable(table[i],tableColums[i],cur,conn)
    query = buildInsertionQuery(data, table, gameid)
    executeQuery(query, cur, conn)
    cur.close()
    
def executeQuery(query, cur, conn):
    """
    Executes a given query on the host defined by the connection using the cursor. Throws error on failure and exits the programm.
    ----------
    Parameters
    ----------
        query (str):                The query to be executed in string form.
        conn    (connection):       Handles the connection to a MariaDB or MySQL database server. It encapsulates a database session.
        cur     (cursor):           Executes SQL statements and procedures, and manages fetching results.
    ----------
    """

    try:
        cur.execute(query)
        conn.commit()
        #TODO: Log query here.
    except mariadb.Error as e:
        cur.close()
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def createTable(table: str, columns: dict, cur, conn):
    try:
        Query = "CREATE TABLE " + table + " (" 
        for key, value in columns.items():
            Query += key + " " + value + ","
        Query[-1] = ")"
        Query += ";"
        cur.execute(Query)
        conn.commit()
    except mariadb.Error as e:
        cur.close()
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def isTableCreated(table: str, cur, conn):
    try: 
        cur.execute("SHOW TABLES LIKE \""+table+"\";")
        conn.commit()
        isTable = cur.fetchone()

        if isTable is None:
            return False

        return True

    except mariadb.Error as e:
        cur.close()
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def buildInsertionQuery(data, table: str, gameid):
    """
    Builds a query for later use from the data, key and tablename
    ----------
    Parameters
    ----------
        data (array):               Array that contains all data to be inserted into the table
        gameid (int):               Primary or part of the composite key for the Database tables
        table (str):                Name of the table, used for selecting the pattern to insert.
    ----------
    Return
    ----------
        query (str):                The generated query.
    ----------
    """
    
    prefix = "INSERT INTO "

    match table:
        case "metadata":
            columns = "(gameid, patch, date, duration)"
            values  = data[0], data[1], data[2], data[3]

        case "teamdata":
            columns =   ("(gameid, teamid, ban1, ban2, ban3, ban4, ban5, barons,"
                        "dragons, herald, grubs, firstbl, firstdr, firstto, firstbr, win)")
            bans    = ','.join(data[0])
            values  = gameid, data[3], bans, data[1], data[2], data[4], data[5], data[6], data[7], data[8], data[9], data[10]

        case "playerdata":
            columns =   ("(gameid, playerid, teamid, champ, summ1, summ2, item1, item2, item3, item4,"
                        "item5, item6, item7, rune1, rune2, rune3, rune4, rune5, rune6, cwards_bought,"
                        "wards_placed, wards_destroyed, vision_score, minions_killed, own_jng_kill,"
                        "ene_jng_kill, kills, deaths, assists, damage_dealt, gold_earned, turret_dmg, team)")

            pid     = data[0][1]
            # Converts the values of a Dictionary into Tuples, then into a string 
            #   and finally strips the brackets away
            items   = str(tuple(data[4])).strip("()").replace("\"", "") # For some reason items adds a \ before " if we don't filter them out now...
            runes   = str(tuple(data[5])).strip("()")
            values  = gameid, pid, data[19], data[1], data[2], data[3], items, runes, data[6], data[7], data[8], data[9], data[10],\
                        data[11], data[12], data[13], data[14], data[15], data[16], data[17], data[18], data[20]
    query   = prefix + table + " " + columns + " VALUES " + str(values).replace("\"", "") + ";"
    print(query)
    return query
    

    
