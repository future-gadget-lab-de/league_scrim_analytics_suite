"""helperfile for input/output functionality. Currently has methods for reading/writing
- raw
- .conf
- .json
- .sql
"""

import os, pathlib, json, requests, csv, sys
from loguru import logger
    
def readSettingsFile(rel_path_with_name: str) -> dict[str, str]:
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
    #FIX: This prints the Password, that is not good.
    logger.trace("Finished readSettingsFile Function with Output: "+ str(config))
    return config

def writeSettingsFile(settings: dict[str, str], rel_path_with_name: str) -> None:
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
    if not os.path.isfile(relPathToFile):
        return list()

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


def requestJsonFile(linkToJson: str, saveLocation: str | None = None) -> dict:
    """request the json body of a provided link.

    Parameters
    ----------
    linkToJson : str
        link to a .json body, to request
    saveLocation : str, optional
        when passed, saves the resulting json body
    
    Returns
    -------
    data_dict : dict
        the json in dict format
    """
    logger.trace("Started requestjsonfile function with link: " + linkToJson)
    logger.debug("Json file gets downstreamed.")
    data_url = linkToJson
    data_response = requests.get(data_url)
    logger.debug("You got a "+str(data_response.status_code) +" reponse with the body:\n"+data_response.__str__())
    if data_response.status_code != 200:
        logger.error("the requested .json body said no! "+ str(data_response.status_code)+": "+data_response.reason) 
        raise FileNotFoundError("The requested .json body said no! "+ str(data_response.status_code)+": "+data_response.reason)
    data_dict = data_response.json()
    if saveLocation is not None:
        os.makedirs(os.path.dirname(relPathToJson), exist_ok=True)
        with open(relPathToJson, 'w', encoding="utf-8") as data:
            json.dump(data_dict, data)
        logger.debug("Written json to dict")
    logger.trace("Finished rejoadjsonfiles function with output: " + str(data_dict))
    return data_dict

def readJsonFile(pathToJson: str) -> dict:
    """reads a passed json file.

    Parameters
    ----------
    pathToJson : str
        rel path to a json file
    
    Returns
    -------
    data_dict : dict
        the json in dict format
    """
    if not os.path.isfile(pathToJson):
        return dict()

    logger.trace("Started readjsonfiles function with inputs path: " +pathToJson)
    with open(pathToJson, encoding="utf-8") as data:
        logger.debug("Read Json: " + pathToJson)
        logger.trace("Finished rejoadjsonfiles function with output: " + str(data))
        return json.load(data)

#TODO: Rewrite Logging
def readSQLFile(relPathtoFile: str) -> list[str]:
    """imports a .sql file.

    imports each query of a passed .sql file as a list of strings

    Parameters
    ----------
    relPathtoFile : str
        relative path to the .sql file
    
    Returns
    -------
    queries : list[str]
        a list of sql queries as strings
    
    """

    sql_lines = readFileByLine(relPathtoFile)
    queries = list()

    query = ""
    for line in sql_lines:
        # skip empty lines
        if line.strip() == "":
            continue
        # skip commented lines
        if line.startswith("--"):
            continue
        
        query += line

        if line.endswith(";"):
            queries.append(query)
            query = ""

    logger.debug("loaded the file: %s", relPathtoFile)
    return queries
