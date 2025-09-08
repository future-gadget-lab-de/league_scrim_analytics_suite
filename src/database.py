import mariadb
import sys


def buildConnection(conn_params):
    conn_params['port'] = int(conn_params['port']) 
    connection = mariadb.connect(**conn_params)
    cursor = connection.cursor()
    return connection, cursor

def insertMetadata(gameid, patch, date, duration,conn_params):
    # establish a connection
    connection, cursor  = buildConnection(conn_params)
    # Build querey
    basequery           = "INSERT INTO metadata () VALUES"
    values              = gameid, patch, date, duration
    value_string        = str(values)
    query               = basequery + " " + value_string
    # Execute query
    executeQuery(query, cursor, connection)

def insertTeamdata(conn_params):
    # establish a connection
    connection, cursor  = buildConnection(conn_params)
    basequery           = "INSERT INTO metadata (gameid, patch, date, duration) VALUES"
    values              = 
    value_string        = str(values)
    query               = basequery + " " + value_string
    # Execute Query
    executeQuery(query, cursor, connection)

def executeQuery(query, cursor, connection):
    try:
        cursor.execute(query)
        connection.commit()
        #TODO: Log query here.
        cursor.close()
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)



def buildQuery(method, data):
    #TODO: Build query here.
    return true