"""contains the plugin support"""

import sys, os
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

from loguru import logger
from src.core.io.wrapper import executeSelectQuery
from src.utils.io import readSQLFile, readJsonFile
from src.utils.path import transformPathtoFileList
from src.utils.module import import_from_path, iter_defined_members
from src.utils.func import param_names

mod_location_c = "templates/plugins"
"""a constant for the path, where the program will check for plugins"""

# function only useful, if GUI is used --> simpler GUI 
def getPossiblePlots(queries: str) -> list[list[dict]]: # [ all mods [ their funcs : their args ]]
    """calculates dependant on a sql query, which possible plots there are
    
    Parameters
    ----------
    queries : str
        a sql query as a string

    Returns
    -------
    data : list[list[str]]
        a list of all modules with their funcs

    """
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
            result_list += [getData(module_dict[plugin], plugin)]

    return result_list

def getPlugins(specific: list[str] = []) -> dict:
    """returns a dict of all modules in plugins, with name as key and module as value.
    
    Parameters
    ----------
    specific : list[str], optional
        a list of modules we want to check only for
        
    Returns
    -------
    modules : dict
        name as keys, modules as values of the plugins folder
        
    """

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
    """returns the identification list-tuple of a dataframe

    Parameters
    ----------
    data : list[pd.DataFrame]
        any list of pandas dataframe

    Returns
    -------
    ident : list[tuple]
        the ident of the passed dataframe
    
    """
    # init the header for the dataframe: DF IDENT
    DF_ident = list()
    for DF in data:
        dtype_list = list()
        for col in DF.columns.tolist():
            dtype_list.append(str(DF[col].dtype))
        
        DF_ident.append(tuple(dtype_list))
    return DF_ident

def isLayoutApplicable(data: list[pd.DataFrame], plug_module) -> bool:
    """checks if a module is applicable for a certain dataframe
    
    Parameters
    ----------
    data : list[pd.DataFrame]
        any list of pandas dataframes
    plug_module
        any module of the plugins folder

    Returns
    -------
    isApplicable : bool

    """
    # iterate over all modules
    
    # get members of that module
    member = iter_defined_members(plug_module)
    DF_ident = getDataFrameIdent(data)

    # extract the sample layout
    layout = plug_module.__dict__["input_layout_c"]

    # check for compatibility
    while layout:
        if layout == DF_ident:
            return True

        if not plug_module.__dict__["accept_less_c"]:
            return False

        layout.pop(-1)
    
    return False

def getData(plug_module, modname: str) -> list[dict]:
    """returns a dict with the members of a module for further use
    
    Parameters
    ----------
    plug_module
        a module, which is located in the plugins folder
        
    Returns
    -------
    use_dict : dict
        a dict containing name and member as key/value
        
    """

    member = iter_defined_members(plug_module)

    this_modules_funcs = list()


    # check every module for compatibility
    for name, val in member:
        if callable(val):
            this_modules_funcs.append({
                name:   val, 
                "args": param_names(val),
                modname:plug_module 
            })

    return this_modules_funcs

    
def ApplyTemplate(pathToTemplateFile: str, customLocation: str = "", customSize: tuple[int, int] = tuple()):
    """
    this method applys certain modules in the plugin folder as expressed 
    in the procedure .json file.

    Parameters
    ----------
    pathToTemplateFile : str
        the path to the .json procedure
    customLocation : str, optional
        if passed, saves the picture generated into the passed path, 
        instead of the location specified in the plugin file.
    
    """

    template_dict = readJsonFile(pathToTemplateFile)
    if not template_dict:
        logger.error("no template file found.")
        raise FileNotFoundError("no template file found.")
    queries_final = list()

    for sql_file in template_dict["SQL_files_location"]:
        queries = readSQLFile(sql_file)
        queries_final += queries

    DF_list: list[pd.DataFrame] = list()

    for query in queries_final:
        DF_list.append(executeSelectQuery(query))


    for module in template_dict["modulenames"].keys():

        executePlugin(DF_list, module, customLocation, customSize, template_dict["modulenames"][module])



def executePlugin(frames: pd.DataFrame, plugname: str, customLocation: str = "", customSize: tuple[int, int] = tuple(), args: dict = {}):
    plugin_instance = getPlugins([plugname])

    if isLayoutApplicable(frames, plugin_instance[plugname]):
        plugin_dictl = getData(plugin_instance[plugname], plugname)

        plotfunction = plugin_dictl[0][list(plugin_dictl[0].keys())[0]]

        is_module_aggregated = len(plugin_dictl) > 1
        if is_module_aggregated:
            aggfunction = plugin_dictl[1][list(plugin_dictl[1].keys())[0]]
            frames = aggfunction(frames)

        if customLocation:
            plugin_instance[plugname].location_c = customLocation

        if customSize:
            plugin_instance[plugname].size_c = customSize

        plotfunction(frames, **args)

