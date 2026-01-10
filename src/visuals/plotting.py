import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

from src.database.wrapper import executeSelectQuery
from src.database.queries import returnSelectQuery


def buildAnalyticsFigure(player: str, feature: str, dim: tuple[int], diagram: str = "line") -> None:
    """builds a diagram for a given player/feature relation. uses the internal data
    
    Parameters
    ----------
    player : str
        the player, of which the diagram is wanted
    feature : str
        a numerical feature
    dim : tuple[int]
        the dimensions of the diagram in int x int
    diagram : str, optional
        a specifier for a diagram. supported: line, histo
        
    """

    query_player = returnSelectQuery("playerdata",[feature],f"playerid='{player}'")
    query_date = returnSelectQuery("metadata",["date","gameid"])

    data_player = executeSelectQuery(query_player)
    data_date = executeSelectQuery(query_date)
    dpi = 100
    figsize = (float(dim[0])/float(dpi), float(dim[1])/float(dpi))
    
    data = data_player.join(data_date)
    plt.figure(dpi, figsize)

    if diagram == "line":

        data = data.groupby("date", as_index=False).mean(numeric_only=True)
        plt.plot(data["date"], data[feature], linestyle="-", marker='o')
        plt.xlabel("date")

    elif diagram == "histo":
        data = data.sort_values(["gameid"])
        plt.bar([str(gameid) for gameid in data["gameid"].values.tolist()], data[feature].values.tolist())

    plt.ylabel(feature)
    plt.grid()
    os.makedirs(os.path.dirname(f"gamefiles/{feature}_{player}_{diagram}.png"), exist_ok=True)
    plt.savefig(f"gamefiles/{feature}_{player}_{diagram}.png")
    plt.close()

