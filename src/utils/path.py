"""helperfile for providing path managing methods.
- conversion to rel path
- listing of a filetree
"""

import os, sys, pathlib
from loguru import logger

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
    logger.trace("Finished transformPathtoFileList function with output: " + str(PathToFolder))

    relPathToFolder = PathToFolder
    if os.path.isabs(PathToFolder):
        relPathToFolder = getRelPath(PathToFolder)

    if os.path.isfile(relPathToFolder):
        files = [relPathToFolder]
    else: # if it is a directory
        files = list_relative_filepaths(relPathToFolder)

    if len(files) == 0:
        err_msg = "There are no files provided through args. Adjust the Path!"
        logger.error(err_msg)
        raise Exception(err_msg)
    logger.trace("Finished transformPathtoFileList function with output: " + str(files))
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