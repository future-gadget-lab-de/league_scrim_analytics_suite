"""the file, which mainly manages the data extraction process"""

import pandas as pd
from enum import Enum
from loguru import logger
from src.core.meta import GameTable, TimeTable, ImportType
from src.core.process.pipelines.client import ClientKeys, tableTypeForClient, needsAggClient, needsMetaDataClient
from src.core.process.pipelines.matchv5 import MatchV5Keys, tableTypeForMatchV5, needsAggMatchV5, needsMetaDataMatchV5
from src.utils.pandas import dropListEntries, mergeTables, indexByOneVariable, concatOnPrefixes

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

pipeToAgg: dict[ImportPipeline, dict] = {
    ImportPipeline.CLIENT: needsAggClient,
    ImportPipeline.MATCHV5: needsAggMatchV5
}
"""dict, which maps the pipeline to the aggregation helper"""

pipeToMeta: dict[ImportPipeline, dict] = {
    ImportPipeline.CLIENT: needsMetaDataClient,
    ImportPipeline.MATCHV5: needsMetaDataMatchV5
}
"""dict, which maps the pipeline to the metapath helper"""

def classify(member: ClientKeys | MatchV5Keys) -> GameTable | TimeTable:
    """classifys the GameTabletype for a Key
    
    Parameters
    ----------
    member : ClientKeys | matchV5Keys
        the member of one of the enums
        
    Returns
    -------
        the table, which it belongs to
        
    """
    logger.trace(f"classified the member {member.value}.")
    # the client case
    if isinstance(member, ClientKeys):
        return tableTypeForClient[member]
    # the matchv5 case
    return tableTypeForMatchV5[member]

def getData(
    data:    dict, 
    pathKey: MatchV5Keys | ClientKeys, 
    typ:     ImportType,
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
    agg : bool, optional
        if passed, the tables gets aggregated with indexbyoneVariable
    
    Returns
    -------
    dataframe : pd.DataFrame
        the resulting table
    
    """
    logger.trace("Start normalizing the raw data dict via pandas.")
    normalizedDf = pd.json_normalize(
        data,
        record_path=pathKey.value,
        meta=metaKey,
        sep="_"
    )

    listlessDf = dropListEntries(normalizedDf)
    
    if agg:
        logger.debug("Start aggregating the resulting datatable.")
        match typ:
            case ImportType.GENERAL:
                return indexByOneVariable(listlessDf, "_".join(metaKey[0]))
            case ImportType.TIMELINE:
                return concatOnPrefixes(listlessDf, [
                    "participantFrames_1_",
                    "participantFrames_2_",
                    "participantFrames_3_",
                    "participantFrames_4_",
                    "participantFrames_5_",
                    "participantFrames_6_",
                    "participantFrames_7_",
                    "participantFrames_8_",
                    "participantFrames_9_",
                    "participantFrames_10_",
                ], "participantid")
        
    return listlessDf

def extractRawTables(data: dict, pipe: ImportPipeline, typ: ImportType) -> dict[GameTable, pd.DataFrame]:
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
    logger.debug("Start the extraction process for the raw json dict.")
    METADATA: list[pd.DataFrame]   = []
    PLAYERDATA: list[pd.DataFrame] = []
    TEAMDATA: list[pd.DataFrame]   = []
    FRAMEDATA: list[pd.DataFrame]  = []
    EVENTDATA: list[pd.DataFrame]  = []

    for path in pipe.value:
        if not isinstance(classify(path),typ.value):
            continue

        logger.debug(f"extracting the part of the json, according to {path.value}.")
        metaKey = None
        aggregation: bool = (path in pipeToAgg[pipe])
        if aggregation:
            metaKey: list[list[str]] = [pipeToAgg[pipe][path]]
        if path in pipeToMeta[pipe]:
            metaKey: list[list[str]] = [pipeToMeta[pipe][path]]
        table: pd.DataFrame = getData(
                data=data,
                pathKey=path,
                typ=typ,
                metaKey=metaKey,
                agg=aggregation
        )

        match classify(path):
            case GameTable.TEAM:
                TEAMDATA.append(table)
            case GameTable.PLAYER:
                PLAYERDATA.append(table)
            case GameTable.META:
                METADATA.append(table)
            case TimeTable.FRAME:
                FRAMEDATA.append(table)
            case TimeTable.EVENT:
                EVENTDATA.append(table)

    return {
        GameTable.META:   mergeTables(METADATA), 
        GameTable.TEAM:   mergeTables(TEAMDATA), 
        GameTable.PLAYER: mergeTables(PLAYERDATA),
        TimeTable.FRAME:  mergeTables(FRAMEDATA), 
        TimeTable.EVENT:  mergeTables(EVENTDATA)
    }

