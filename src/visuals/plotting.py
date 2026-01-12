import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

from src.database.wrapper import executeSelectQuery
from src.database.queries import returnSelectQuery
from src.database.mariadb.sqltemplates.template import importSQLQueries
from src.utils import transformPathtoFileList, import_from_path, iter_defined_members, param_names, reloadjsonfiles

mod_location_c = "plugins"

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

# function only useful, if GUI is used --> simpler GUI 
def getPossiblePlots(queries: str) -> list[list[dict]]: # [ all mods [ their funcs : their args ]]

    template_paths = transformPathtoFileList(mod_location_c)

    DF_list: list[pd.DataFrame] = list[pd.DataFrame]()
    for query in queries:
        DF_list.append(executeSelectQuery(query))

    # init the header for the dataframe
    DF_ident = list()
    for DF in DF_list:
        dtype_list = list()
        for col in DF.columns.tolist():
            dtype_list.append(str(DF[col].dtype))
        
        DF_ident.append(tuple(dtype_list))

    module_list = list()
    functions_to_consider = list()
    imported_files = list()

    for file in template_paths:
        module_str = file.split("/")[-1].removesuffix(".py")
        if module_str != "__init__" and not file.endswith(".pyc"):
            imported_files.append([module_str, file])
            module_list.append(import_from_path(module_str, file))

    result_list = list()

    for i, mod in enumerate(module_list):
        
        member = iter_defined_members(mod)

        this_modules_funcs = list()

        if mod.__dict__["input_layout_c"] == DF_ident:
            for name, val in member:
                if callable(val):
                    this_modules_funcs.append({
                        name:   val, 
                        "args": param_names(val), 
                        "module": imported_files[i][0],
                        "loc":  imported_files[i][1]}
                    )

            result_list.append(this_modules_funcs)
            continue

        if mod.__dict__["accept_less_c"]:
            layout = mod.__dict__["input_layout_c"]
            while layout:
                if layout == DF_ident:
                    for name, val in member:
                        if callable(val):
                            this_modules_funcs.append({
                                name:   val, 
                                "args": param_names(val), 
                                "module": imported_files[i][0],
                                "loc":  imported_files[i][1]}
                            )
                    
                    break
                layout.pop(-1)


        result_list.append(this_modules_funcs)

    return result_list

def ApplyJson(path):
    inf = reloadjsonfiles(path, "")

    queries = importSQLQueries(inf["SQL_files_location"][0])

    data = getPossiblePlots(queries)
    print(data)

    for mod in inf["modulenames"].keys():
        if str(mod) == data[1][0]["module"]:
            print("Ausgeführt")
            data[1][0]["simpleHistoLSAS"](executeSelectQuery(queries[0]))




