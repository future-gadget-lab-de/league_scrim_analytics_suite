import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

from src.core.ops import executeSQLFiles
from src.database.queries import returnSelectQuery
from src.database.execution import buildConnection,executeQuery,getCursorSelect
from src.database.sqltemplates.template import importSQLQueries

def sqlDictToPandas(SQL_DATA: list[dict]) -> pd.DataFrame:
    data_dict = dict()
    for key in SQL_DATA[0].keys():

        data_list = list()

        for data in SQL_DATA:
            data_list.append(data[key])
        
        data_dict[key] = data_list

    return pd.DataFrame(data_dict)

def buildAnalyticsFigure(player: str, mode: str, dim: tuple[int]):

    query_player = returnSelectQuery("playerdata",[mode],f"playerid='{player}'")
    query_date = returnSelectQuery("metadata",["date","gameid"])

    conn,cur = buildConnection()

    executeQuery([query_player], conn, cur)
    output_player = getCursorSelect(cur)

    executeQuery([query_date], conn, cur)
    output_date = getCursorSelect(cur)

    conn.close()
    cur.close()

    data_player = sqlDictToPandas(output_player)
    data_date = sqlDictToPandas(output_date)

    data = data_player.join(data_date)

    data = data.groupby("date", as_index=False).mean(numeric_only=True)

    dpi = 100
    figsize = (float(dim[0])/float(dpi), float(dim[1])/float(dpi))

    plt.figure(dpi, figsize)

    plt.plot(data["date"], data[mode], linestyle="-", marker='o')
    plt.xlabel("date")
    plt.ylabel(mode)
    plt.title("Line Chart Example")
    plt.grid()
    plt.savefig(f"gamefiles/{mode}_{player}.png")
    plt.close()

