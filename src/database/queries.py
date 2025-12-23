from src.match import loadMatchData

def returnInsertQuery(table: str, data: dict) -> str:
    query = "INSERT INTO " + table + " ("
    
    for key in data.keys():
        query += str(key) + ","
    query = query.removesuffix(",")
    
    query += ") VALUES "

    #for key in data.keys():
    #    query += str(data[key]) + ","
    #query = query.removesuffix(",")

    query += str(tuple(data.values()))

    query += ";"

    return query

def returnMatchfileInsert(relPathtoFile)-> list[str]:
    metadata, playerdata, blueteamdata, redteamdata, data_file = loadMatchData(relPathtoFile)

    queries = list()

    queries.append(returnInsertQuery("metadata",metadata))
    for playerdict in playerdata:
        queries.append(returnInsertQuery("playerdata",playerdict))
    queries.append(returnInsertQuery("teamdata",blueteamdata))
    queries.append(returnInsertQuery("teamdata",redteamdata))

    return queries