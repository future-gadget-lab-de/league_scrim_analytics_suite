"""shortening pipelines or methods, which are defined somewhere for general purpose"""

from src.core.io.mariadb import executeSQLFile
from src.utils.path import transformPathtoFileList
from src.core.process.reading import importMatchfiles
from src.core.process.writing import writeData

def importPipeline(pathToFolder: str) -> None:
    """importing matchfiles generalized for some path
    
    Parameters
    ----------
    pathToFolder : str
        a path (rel or abs) to some folder or file
    
    """
    files = transformPathtoFileList(pathToFolder)

    for file in files:
        table = importMatchfiles(file)
        writeData(table)

def executeSQLFiles(pathToFolder: str) -> None:
    """executes a number of sqlfiles
    
    pathToFolder : str
        a path (rel or abs) to some folder or file
        
    """
    files = transformPathtoFileList(pathToFolder)
    
    for file in files:
        executeSQLFile(file)
