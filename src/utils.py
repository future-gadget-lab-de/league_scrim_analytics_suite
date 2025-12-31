import logging
logger = logging.getLogger(__name__)

import os, pathlib, json, requests, csv
#TODO: Rewrite Logging
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

    abs_path_object = pathlib.Path(absPath)
    
    return os.path.relpath(str(abs_path_object), start=os.getcwd())

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
    fields = list(data.keys())
    os.makedirs(os.path.dirname(path_to_csv), exist_ok=True)
    with open(path_to_csv, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writerows([data])  # Write data rows

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
    config = dict()
    config_by_line = readFileByLine(rel_path_with_name)    
    
    for line in config_by_line:
        setting = line.replace(" ", "").split("=")   # remove whitespace and split
        config[setting[0]] = setting[1]    # build dict 
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
    lines = [f"{key}={value}" for key, value in settings.items()]
    
    base_path = os.path.abspath(os.getcwd())
    full_path = os.path.join(base_path, rel_path_with_name)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as conf_file:
        conf_file.write("\n".join(lines))


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
    
    filelist = []
    with os.scandir(path) as ents:
        for e in ents:
            if e.is_dir() or "invalid" in e.name:
                continue
            else:
                filelist.append(e.name)
    filename=filelist[0]
    matchfile = path + filename
    return matchfile

    
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
    try:    
        with open(relPathToFile) as file:
            lines = [line.rstrip() for line in file]  # remove \n
            return lines
    except:
        print("[ERROR] file: " + relPathToFile + " can't be read")
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
    path_hierarchy = dest.split("/")
    rel_path_to_folder = dest.removesuffix(path_hierarchy[-1])
    
    if not os.path.isdir(rel_path_to_folder):
        pathlib.Path(rel_path_to_folder).mkdir(parents=True, exist_ok=True)

    os.rename(file, dest)


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
    if os.path.isabs(path):
        raise ValueError("Path must be relative")

    search_path = os.path.abspath(path)
    base_path = os.getcwd()

    if not os.path.isdir(base_path):
        return []

    filepaths: list[str] = []
    for root, _, files in os.walk(search_path):
        for filename in files:
            absolute_path = os.path.join(root, filename)
            relative_path = os.path.relpath(absolute_path, start=base_path)
            filepaths.append(relative_path)

    return filepaths

def reloadjsonfiles(relPathToJson: str, linkToJson: str) -> dict:
    """loads (or reloads) a specified .json

    this method checks, if a json is existens and returns it. if it doesnt
    exist, it gets scraped.

    Parameters
    ----------
    relPathToJson : str
        relative path to the .json file, which is checked for
    linkToJson : str
        link to the corresponding online source
    
    Returns
    -------
    data_dict : dict
        the json, from one of the sources above
    """

    # check if the file is already dumped
    if os.path.isfile(relPathToJson):
        with open(relPathToJson) as data:
            # print("read json")
            return json.load(data)
    else:
        logger.debug("Json file is not present. Downstreaming a new one.")
        data_url = linkToJson
        data_response = requests.get(data_url)
        data_dict = data_response.json()

        os.makedirs(os.path.dirname(relPathToJson), exist_ok=True)

        with open(relPathToJson, 'w') as data:
            # print("dumped json")
            json.dump(data_dict, data)

        return data_dict

