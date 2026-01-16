import os, pathlib, json, requests, csv, sys
from loguru import logger
import importlib.util
import inspect

def param_names(fn):
    return [p.name for p in inspect.signature(fn).parameters.values()]

def iter_defined_members(module) -> list[tuple]:
    stuff = list()
    mod = module
    for name, obj in vars(mod).items():
        if name.startswith("_"):
            continue
        if inspect.ismodule(obj):
            continue
        if inspect.isfunction(obj) or inspect.isclass(obj):
            if getattr(obj, "__module__", None) != mod.__name__:
                continue
        
        stuff.append((name,obj))
    
    return stuff

def import_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def transformPathtoFileList(PathToFolder: str) -> list[str]:
    """
    accepts a path which contains a folder or file
    and accepts both rel and abs path. it returns a list
    of provided files as a rel path.

    Parameters
    ----------
    PathToFolder : str
        provided path

    Returns
    -------
    files : list[str]
        a list of rel paths to the files
    
    """
    relPathToFolder = PathToFolder
    if os.path.isabs(PathToFolder):
        relPathToFolder = getRelPath(PathToFolder)

    if os.path.isfile(relPathToFolder):
        files = [relPathToFolder]
    else: # if it is a directory
        files = list_relative_filepaths(relPathToFolder)

    if len(files) == 0:
        raise Exception("There are no files provided through args. Adjust the Path!")
        sys.exit(1)

    return files


def getRelPath(absPath: str) -> str:
    """
    returns the relative path for some absolute path

    Parameters
    ----------
    absPath : str
        the absolute path, which is to be convert

    Returns
    -------
    relPath : str
        the resulting relative path
    
    """
    logger.trace("Starting getRelPath function with input: " + absPath)

    abs_path_object = pathlib.Path(absPath)
    relPath = os.path.relpath(str(abs_path_object), start=os.getcwd())

    logger.trace("Finished getRelPath function with Output: " + relPath)
    return relPath

def addDictToCsv(data: dict, path_to_csv: str) -> None:
    """
    adds the data of a passed dict to a passed .csv

    Parameters
    ----------
    data : str
        the data which will get imported
    path_to_csv : str
        the relative path to the .csv file
    """
    logger.trace("Starting addDictToCsv function with path:" + path_to_csv + " and data_dict: "+ str(data))

    fields = list(data.keys())
    
    os.makedirs(os.path.dirname(path_to_csv), exist_ok=True)
    logger.debug("Attempting to write file: " + path_to_csv)

    with open(path_to_csv, mode='a', newline='',encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writerows([data])  # Write data rows

    logger.info("Written file: " + path_to_csv)
    logger.trace("Finished addDictToCsv function")
    
def readSettingsFile(rel_path_with_name: str) -> dict:
    """
    Reads a passed .conf file

    Parameters
    ----------
    rel_path_with_name : str
        the relative path to a config file
    
    Returns
    -------
    settings : dict
        the dictionary, containing the settings
    
    """
    logger.trace("Starting readSettingsFile Function with Input: " +rel_path_with_name)
    config = dict()
    config_by_line = readFileByLine(rel_path_with_name)    
    
    for line in config_by_line:
        setting = line.replace(" ", "").split("=")   # remove whitespace and split
        config[setting[0]] = setting[1]    # build dict 
        logger.trace("Add the following value to config-dict.: "+ str(setting[1]))
    logger.trace("Finished readSettingsFile Function with Output: "+ str(config))
    return config

def writeSettingsFile(settings: dict, rel_path_with_name: str) -> None:
    """
    Writes the given lines to a .conf file at the provided relative path.

    Parameters
    ----------
    lines : list[str]
        Lines to write to the config file.
    rel_path_with_name : str
        Relative path including the filename (e.g. "config/lsas.conf").
    """
    logger.trace("Starting writeSettingsFile Function")

    lines = [f"{key}={value}" for key, value in settings.items()]
    
    base_path = os.path.abspath(os.getcwd())
    full_path = os.path.join(base_path, rel_path_with_name)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as conf_file:
        conf_file.write("\n".join(lines))
        logger.debug("Written config file: " + full_path)
        logger.trace("Finished writeSettingsFile function")
def findFile(path: str) -> str:
    """
    Finds the first file in the folder given by path.
   
    Parameters
    ----------
    path : str               
        the relative path, to a folder

    Returns
    -------
    matchfile : str          
        relative path for the file

    """
    logger.trace("Starting findFile function with Input: " + path)
    filelist = []
    with os.scandir(path) as ents:
        for e in ents:
            if e.is_dir() or "invalid" in e.name:
                continue
            else:
                filelist.append(e.name)
    filename=filelist[0]
    file = path + filename
    logger.trace("Finished findFile function with Output: " + file)
    return file
#NOTE Continue here
def readFileByLine(relPathToFile) -> list[str]:
    """
    Read a file as an array of string lines.

    Parameters
    ----------
    relPathToFile : str
        The relative path to a file, which is to be read.

    Returns
    -------
    lines : list[str]
        A list, containing each line per entry in the list.   
    
    """
    logger.trace("Started readFileByLine function with Input: " + relPathToFile)
    try:    
        with open(relPathToFile, encoding="utf-8") as file:
            lines = [line.rstrip() for line in file]  # remove \n
            logger.trace("Finished readFileByLine function with Output:" + str(lines))
            return lines
    except:
        logger.critical("file: " +relPathToFile + "cannot be read.")
        exit(1)



def moveFile(file, dest: str) -> None:
    """
    Moves a file, to the provided destination
    
    Parameters
    ----------
    file : str                  
        The filename, which is to move.
    dest : str             
        The destination as a relative path (containing the new name).
    """
    logger.trace("Started moveFile function with Inputs file: " + str(file) + " and destination: " +dest)
    path_hierarchy = dest.split("/")
    rel_path_to_folder = dest.removesuffix(path_hierarchy[-1])
    
    if not os.path.isdir(rel_path_to_folder):
        logger.info("Created Folder: " + rel_path_to_folder)
        pathlib.Path(rel_path_to_folder).mkdir(parents=True, exist_ok=True)

    os.rename(file, dest)
    logger.debug("Moved file : " + str(file) + " to " + dest)
    logger.trace("Finished moveFile function")

def list_relative_filepaths(path: str) -> list[str]:
    """
    Collects all files in a directory tree and returns their paths relative to the given base path.

    Parameters
    ----------
    path : str                 
        The base directory to scan (relative path only).
    
    Returns
    -------
    filepaths : list[str]
        List of file paths relative to the provided base directory.

    """
    logger.trace("Started list_relative_filepaths function with Input: " +path)
    if os.path.isabs(path):
        err_msg = "Path must be relative"
        logger.error(err_msg)
        raise ValueError(err_msg)

    search_path = os.path.abspath(path)
    base_path = os.getcwd()

    if not os.path.isdir(base_path):
        logger.debug("No files found! Exiting list_relative_filepaths")
        return []

    filepaths: list[str] = []
    for root, _, files in os.walk(search_path): #NOTE Why the ,_, ?
        for filename in files:
            absolute_path = os.path.join(root, filename)
            relative_path = os.path.relpath(absolute_path, start=base_path)
            filepaths.append(relative_path)
    logger.trace("Finished list_relative_filepaths Function with output: " + str(filepaths))
    return filepaths

def loadjsonfiles(relPathToJson: str, linkToJson: str | None = None, forcereload: bool = False) -> dict:
    """loads (or reloads) a specified .json

    this method checks, if a json is existens and returns it. if it doesnt
    exist, it gets scraped.

    Parameters
    ----------
    relPathToJson : str
        relative path to the .json file, which is checked for
    linkToJson : str, optional
        link to the corresponding online source
    
    Returns
    -------
    data_dict : dict
        the json, from one of the sources above
    """
    
    # check if the file is already dumped
    if os.path.isfile(relPathToJson) and not forcereload:
        logger.trace("Started loadjsonfiles function with inputs path: " +relPathToJson)
        with open(relPathToJson, encoding="utf-8") as data:
            logger.debug("Read Json: " + relPathToJson)
            logger.trace("Finished rejoadjsonfiles function with output: " + str(data))
            return json.load(data)
    
    if linkToJson is not None:

        logger.trace("Started loadjsonfiles function with inputs path: " +relPathToJson + "and link: " + linkToJson)
        logger.debug("Json file is not present. Downstreaming a new one.")
        data_url = linkToJson
        data_response = requests.get(data_url)
        data_dict = data_response.json()
        os.makedirs(os.path.dirname(relPathToJson), exist_ok=True)

        with open(relPathToJson, 'w', encoding="utf-8") as data:
            json.dump(data_dict, data)
        logger.debug("Written json to dict")
        logger.trace("Finished rejoadjsonfiles function with output: " + str(data_dict))
        return data_dict

