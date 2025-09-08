import mariadb
import sys


def buildConnection(conn_params):
    conn_params['port'] = int(conn_params['port']) 
    connection = mariadb.connect(**conn_params)
    cursor = connection.cursor()
    return connection, cursor

def insertData(data, conn_params, gameid, table: str):
    # establish a connection
    connection, cursor  = buildConnection(conn_params)
    # Build query
    query = buildQuery(data, table, gameid)
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

def buildQuery(data, table: str, gameid):
    prefix = "INSERT INTO "

    match table:
        case "metadata":
            columns = "(gameid, patch, date duration)"
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
    query   = prefix + table + columns + " VALUES " + str(values).replace("\"", "")
    return query
    

    
