import pandas as pd
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from enum import Enum
from src.core.team import playerTeamCheck
from src.core.structure import GameTable
from src.core.extracting.client import ClientKeys, tableTypeForClient, needsAggClient, needsMetaDataClient, translationClient
from src.core.extracting.matchv5 import MatchV5Keys, tableTypeForMatchV5, needsAggMatchV5, needsMetaDataMatchV5
from src.utilss.pandas import dropListEntries, mergeTables, indexByOneVariable
from src.database.queries import returnInsertQuery
from src.utils import loadjsonfiles

class ImportPipeline(Enum):
    """possible pipelines, we use currently
    
    Attributes
    ----------
    CLIENT : ClientKeys
        the pipeline for the client dumped data
    MATCHV5 : MatchV5Keys
        the pipeline for the matchv5 gathered data
    
    """
    CLIENT  = ClientKeys
    MATCHV5 = MatchV5Keys

pipeToTrans: dict[ImportPipeline, dict] = {
    ImportPipeline.CLIENT: translationClient

}

pipeToAgg: dict[ImportPipeline, dict] = {
    ImportPipeline.CLIENT: needsAggClient,
    ImportPipeline.MATCHV5: needsAggMatchV5
}

pipeToMeta: dict[ImportPipeline, dict] = {
    ImportPipeline.CLIENT: needsMetaDataClient,
    ImportPipeline.MATCHV5: needsMetaDataMatchV5
}

subTestSet: set[str] = {'championId_0', 'championId_1', 'championId_2', 'championId_3', 'championId_4'}

def classify(member: ClientKeys | MatchV5Keys) -> GameTable:
    # the client case
    if isinstance(member, ClientKeys):
        return tableTypeForClient[member]
    # the matchv5 case
    return tableTypeForMatchV5[member]

def getData(
    data:    dict, 
    pathKey: MatchV5Keys | ClientKeys, 
    metaKey: list[list[str]] | None = None,
    agg:      bool = False,
) -> pd.DataFrame:
    """parses the data according the passed pathKey
    
    Parameters
    ----------
    data : dict
        the raw data, extracted from a .json gamefile
    pathKey : MatchV5Keys | ClientKeys
        the path to the data in the json tree of the gamefile
    metaKey : list[list[str]] | None, optional
        the path to a meta variable. this is only used, if the jsontree contains deeper lists,
        that we have to parse in an extra step.
    
    Returns
    -------
    dataframe : pd.DataFrame
        the resulting table
    
    """
    normalizedDf = pd.json_normalize(
        data,
        record_path=pathKey.value,
        meta=metaKey,
        sep="_"
    )

    listlessDf = dropListEntries(normalizedDf)
    
    if agg:
        return indexByOneVariable(listlessDf, "_".join(metaKey[0]))
        
    return listlessDf


def extractRawTables(data: dict, pipe: ImportPipeline) -> dict[GameTable, pd.DataFrame]:
    """Collects all member of a enum class (see head of this file) and 
    executes these onto a data dict, to extract the data and format it into
    three outcomes: PLAYER-, META- and TEAMDATA
    
    Parameters
    ----------
    data : dict
        the raw data, extracted from a .json gamefile
    className : ImportPipeline
        one of the two classnames above
        
    Returns
    -------
    dataframes : list[pd.DataFrame]
        contains the three major tables: metadata, playerdata, teamdata
        
    """

    METADATA: list[pd.DataFrame]   = []
    PLAYERDATA: list[pd.DataFrame] = []
    TEAMDATA: list[pd.DataFrame]   = []

    for path in pipe.value:

        metaKey = None
        aggregation: bool = (path in pipeToAgg[pipe])
        if aggregation:
            metaKey: list[list[str]] = [pipeToAgg[pipe][path]]
        if path in pipeToMeta[pipe]:
            metaKey: list[list[str]] = [pipeToMeta[pipe][path]]
        table: pd.DataFrame = getData(
                data=data,
                pathKey=path,
                metaKey=metaKey,
                agg=aggregation
        )
        print(table)

        match classify(path):
            case GameTable.TEAM:
                TEAMDATA.append(table)
            case GameTable.PLAYER:
                PLAYERDATA.append(table)
            case GameTable.META:
                METADATA.append(table)

    return {
        GameTable.META:   mergeTables(METADATA), 
        GameTable.TEAM:   mergeTables(TEAMDATA), 
        GameTable.PLAYER: mergeTables(PLAYERDATA)
    }

def translateTables(rawTables: dict[GameTable, pd.DataFrame], pipe: ImportPipeline) -> None:
    """adjusts the passed rawTables according to the translation dict
    
    Parameters
    ----------
    rawTables : dict[GameTable, pd.DataFrame]
        the raw table, we will adjust in this method
    pipe : ImportPipeline
        the pipeline we used in the extraction
        
    """
    translateDict: dict[str,str] = pipeToTrans[pipe]

    for tableType in GameTable:
        # translate into the old layout
        transTablecols = list(translateDict[tableType].keys())
        tablecols = set(rawTables[tableType].columns)
        # insert empty columns, for all missing ones
        if not subTestSet.issubset(tablecols):
            for lostEntry in subTestSet: 
                rawTables[tableType][lostEntry] = "-"
        rawTables[tableType] = rawTables[tableType][transTablecols]
        rawTables[tableType] = rawTables[tableType].rename(translateDict[tableType], axis="columns")

        # aggregate further
        match tableType:

            case GameTable.META:
                patch_list = rawTables[tableType].loc[0,"patch"].split(".")
                rawTables[tableType].loc[0,"patch"] = ".".join(patch_list[0:2]) + ".1"
                rawTables[tableType].loc[0,"date"] = rawTables[tableType].loc[0,"date"][0:10]

            case GameTable.TEAM:
                for i in range(2):
                    rawTables[tableType].loc[i,"win"] = True if (rawTables[tableType].loc[i,"win"] == "Win") else False

            case GameTable.PLAYER:
                for i in range(10):
                    rawTables[tableType].loc[i,"team"] = playerTeamCheck(rawTables[tableType].loc[i,"team"])

