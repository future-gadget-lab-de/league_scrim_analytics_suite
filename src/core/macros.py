from src.core.io.mariadb import executeSQLFile
from src.utils.path import transformPathtoFileList
from src.core.process.reading import importMatchfiles
from src.core.process.writing import writeData

def importPipeline(pathToFolder: str) -> None:

    files = transformPathtoFileList(pathToFolder)

    for file in files:
        table = importMatchfiles(file)
        writeData(table)

def executeSQLFiles(pathToFolder: str) -> None:
    
    files = transformPathtoFileList(pathToFolder)
    
    for file in files:
        executeSQLFile(file)
