import mariadb
import sys

try: #TODO: Load from Config
    # connection parameters
    conn_params = {
        'user' : "",
        'password' : "",
        'host' : "",
        'port' : 3306,
        'database' : ""
    }

    # establish a connection
    connection = mariadb.connect(**conn_params)
    cursor = connection.cursor()
    
    # query

    query = """INSERT INTO metadata (gameid, patch, date, duration) 
    VALUES 
    (7493705947, '15.16', '2025-08-13', '0:33:35')"""
    cursor.execute(query)
    connection.commit()
    cursor.close()

except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
