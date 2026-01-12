import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

from src.database.wrapper import executeSelectQuery
from src.database.mariadb.sqltemplates.template import importSQLQueries
from src.utils import transformPathtoFileList, import_from_path, iter_defined_members, param_names, loadjsonfiles

mod_location_c = "templates/plugins"

# function only useful, if GUI is used --> simpler GUI 
def getPossiblePlots(queries: str) -> list[list[dict]]: # [ all mods [ their funcs : their args ]]

    DF_list: list[pd.DataFrame] = list()
    for query in queries:
        DF_list += [executeSelectQuery(query)]

    functions_to_consider = list()
    imported_files = list()

    # import plugins
    module_dict = getPlugins()

    result_list = list()

    for plugin in module_dict.keys():
        if isLayoutApplicable(DF_list, module_dict[plugin]):
            result_list += [getData(module_dict[plugin])]

    return result_list

def getPlugins(specific: list[str] = []) -> dict:

    template_paths = transformPathtoFileList(mod_location_c)
    module_dict = dict()

    # init all python files as modules
    for file in template_paths:
        module_str = file.split("/")[-1].removesuffix(".py")

        if specific and not module_str in specific:
            continue

        if module_str != "__init__" and not file.endswith(".pyc"):
            module = import_from_path(module_str, file)
            module_dict[module_str] = module

    return module_dict

def getDataFrameIdent(data: list[pd.DataFrame]) -> list[tuple]:
    # init the header for the dataframe: DF IDENT
    DF_ident = list()
    for DF in data:
        dtype_list = list()
        for col in DF.columns.tolist():
            dtype_list.append(str(DF[col].dtype))
        
        DF_ident.append(tuple(dtype_list))
    return DF_ident

def isLayoutApplicable(data: list[pd.DataFrame], plug_module):
    # iterate over all modules
    
    # get members of that module
    member = iter_defined_members(plug_module)
    DF_ident = getDataFrameIdent(data)

    # extract the sample layout
    layout = plug_module.__dict__["input_layout_c"]

    # check for compatibility
    while layout:
        print(layout)
        print(DF_ident)
        if layout == DF_ident:
            return True

        if not plug_module.__dict__["accept_less_c"]:
            return False

        layout.pop(-1)
    
    return False

def getData(plug_module) -> list[dict]:

    member = iter_defined_members(plug_module)

    this_modules_funcs = list()

    # check every module for compatibility
    for name, val in member:
        if callable(val):
            this_modules_funcs.append({
                name:   val, 
                "args": param_names(val)
            })

    return this_modules_funcs

    
def ApplyTemplate(pathToTemplateFile: str, customLocation: str = ""):
    
    template_dict = loadjsonfiles(pathToTemplateFile)
    queries_final = list()

    for sql_file in template_dict["SQL_files_location"]:
        queries = importSQLQueries(sql_file)
        queries_final += queries

    DF_list: list[pd.DataFrame] = list()

    for query in queries_final:
        DF_list.append(executeSelectQuery(query))

    instance_of_plugins = getPlugins(list(template_dict["modulenames"].keys()))

    for module in template_dict["modulenames"].keys():
        print("check if:")
        if isLayoutApplicable(DF_list, instance_of_plugins[module]):
            print("Checked!")
            plugin_dictl = getData(instance_of_plugins[module])

            plotfunction = plugin_dictl[0][list(plugin_dictl[0].keys())[0]]

            is_module_aggregated = len(plugin_dictl) > 1
            if is_module_aggregated:
                aggfunction = plugin_dictl[1][list(plugin_dictl[1].keys())[0]]
                DF_list = aggfunction(DF_list)

            if customLocation:
                instance_of_plugins[module].location_c = customLocation

            plotfunction(DF_list, **template_dict["modulenames"][module])

ApplyTemplate("templates/plots/sample.json", "gg/My.png")
