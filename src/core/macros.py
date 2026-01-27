"""shortening pipelines or methods, which are defined somewhere for general purpose"""

from src.core.io.mariadb import executeSQLFile
from src.utils.path import transformPathtoFileList
from src.core.process.reading import importMatchfiles, translateCentralData
from src.core.meta import ImportType
from src.core.process.writing import writeData

def importPipeline(pathToFolder: str, typ: ImportType) -> None:
    """importing matchfiles generalized for some path
    
    Parameters
    ----------
    pathToFolder : str
        a path (rel or abs) to some folder or file
    
    """
    files = transformPathtoFileList(pathToFolder)

    for file in files:
        table = importMatchfiles(file, typ)
        translateCentralData(table, typ)
        writeData(table, typ)

    

def executeSQLFiles(pathToFolder: str) -> None:
    """executes a number of sqlfiles
    
    pathToFolder : str
        a path (rel or abs) to some folder or file
        
    """
    files = transformPathtoFileList(pathToFolder)
    
    for file in files:
        executeSQLFile(file)
