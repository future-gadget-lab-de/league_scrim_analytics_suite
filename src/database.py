import mariadb
import sys


def buildConnection(conn_params):
    conn_params['port'] = int(conn_params['port']) 
    connection = mariadb.connect(**conn_params)
    cursor = connection.cursor()
    return connection, cursor

def insertMetadata(data ,conn_params, gameid):
    # establish a connection
    connection, cursor  = buildConnection(conn_params)
    # Build query
    query = buildQuery(data, "metadata", gameid)
    print(query) 
    exit()
    # Execute query
    executeQuery(query, cursor, connection)

def insertTeamdata(data, conn_params, gameid):
    # establish a connection
    connection, cursor  = buildConnection(conn_params)
    # Build query
    query = buildQuery(data, "teamdata", gameid)
    print(query) 
    # Execute Query
    # executeQuery(query, cursor, connection)

def executeQuery(query, cursor, connection):
    try:
        cursor.execute(query)
        connection.commit()
        #TODO: Log query here.
        cursor.close()
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def buildQuery(data, table: str, gameid):
    prefix = "INSERT INTO "
    match table:
        case "metadata":
            columns = "(gameid, patch, date duration)"
            values  = data[0], data[1], data[2], data[3]
        case "teamdata":
            columns = "(gameid, teamid, ban1, ban2, ban3, ban4, ban5, \
barons, dragons, herald, grubs, firstbl, firstdr, firstto, firstbr, win)"
            bans    = ','.join(data[0])
            values  = gameid, data[3], bans, data[1], data[2], data[4], data[5], data[6], data[7], data[8], data[9], data[10]
        case "playerdata":
            return false
    query   = prefix + table + columns + " VALUES " + str(values) 
    return query
    