import mariadb
import sys

def insertMetadata(gameid, patch, date, duration,conn_params):
    try:
        # establish a connection)
        conn_params['port'] = int(conn_params['port'])
        connection = mariadb.connect(**conn_params)
        cursor = connection.cursor()
        # query
        basequery       = "INSERT INTO metadata (gameid, patch, date, duration) VALUES"
        values          = gameid, patch, date, duration
        value_string    = str(values)
        query = basequery + " " + value_string
        print(query)
        cursor.execute(query)
        connection.commit()
        cursor.close()

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def executeQuery(query, cursor, connection):
    try:
        cursor.execute(query)
        connection.commit()
        #TODO: Log query here.
        cursor.close()
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)