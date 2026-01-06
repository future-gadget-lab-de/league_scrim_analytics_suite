import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

from src.core.ops import executeSQLFiles


def sqlDictToPandas(SQL_DATA: list[dict]) -> pd.DataFrame:
    data_dict = dict()
    for key in SQL_DATA[0].keys():

        data_list = list()

        for data in SQL_DATA:
            data_list.append(data[key])
        
        data_dict[key] = data_list

    return pd.DataFrame(data_dict)

dates = sqlDictToPandas(executeSQLFiles("src/database/sqltemplates/get_date_of_games.sql"))

print(type(executeSQLFiles("src/database/sqltemplates/get_date_of_games.sql")[0]["date"]))

print(sqlDictToPandas(executeSQLFiles("gamefiles/test.sql")))

df = sqlDictToPandas(executeSQLFiles("gamefiles/test.sql"))

new = df.join(dates)
new.plot(x = "date", y = "cwards_bought", kind="line", marker='o')
print(type(dates["date"]))
plt.show()