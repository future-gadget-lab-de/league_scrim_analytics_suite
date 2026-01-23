"""the file, which mainly manages the data extraction process"""

import pandas as pd
from enum import Enum
from loguru import logger
from src.core.team import playerTeamCheck
from src.core.meta import GameTable
from src.core.process.map import mapId
from src.core.process.pipelines.client import ClientKeys, tableTypeForClient, needsAggClient, needsMetaDataClient, translationClient
from src.core.process.pipelines.matchv5 import MatchV5Keys, tableTypeForMatchV5, needsAggMatchV5, needsMetaDataMatchV5
from src.utils.pandas import dropListEntries, mergeTables, indexByOneVariable
from src.utils.sqlquery import returnInsertQuery

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
"""dict, which maps the pipeline to the translation helper"""

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

gameTableLength: dict[GameTable, int] = {
    GameTable.META: 1,
    GameTable.PLAYER: 10,
    GameTable.TEAM: 2
}

mappables: dict[GameTable, dict[str, list[str]]] = {
    GameTable.META: {},
    GameTable.PLAYER: {
        "summoner": [
            "spell1Id",
            "spell2Id",
        ],
        "perk": [
            "stats_perk0",
            "stats_perk1",
            "stats_perk2",
            "stats_perk3",
            "stats_perk4",
            "stats_perk5",
        ],
        "item": [
            "stats_item0",
            "stats_item1",
            "stats_item2",
            "stats_item3",
            "stats_item4",
            "stats_item5",
            "stats_item6",
        ],
        "champion": [
            "championId"
        ]
    },
    GameTable.TEAM: {
        "champion": [
            "championId_0",
            "championId_1",
            "championId_2",
            "championId_3",
            "championId_4"
        ]
    }
}

subTestSet: set[str] = {'championId_0', 'championId_1', 'championId_2', 'championId_3', 'championId_4'}
"""a set of names to test if contained in the resulting table"""

def classify(member: ClientKeys | MatchV5Keys) -> GameTable:
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
    logger.debug("Start the extraction process for the raw json dict.")
    METADATA: list[pd.DataFrame]   = []
    PLAYERDATA: list[pd.DataFrame] = []
    TEAMDATA: list[pd.DataFrame]   = []

    for path in pipe.value:
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
    logger.trace("Start translation process for the result dataframe.")
    translateDict: dict[str,str] = pipeToTrans[pipe]

    patch_list = rawTables[GameTable.META].loc[0,"gameVersion"].split(".")
    rawTables[GameTable.META].loc[0,"gameVersion"] = ".".join(patch_list[0:2]) + ".1"
    read_patch = rawTables[GameTable.META].loc[0,"gameVersion"]

    for tableType in GameTable:
        # translate into the old layout
        transTablecols = list(translateDict[tableType].keys())
        tablecols = set(rawTables[tableType].columns)
        # insert empty columns, for all missing ones
        if not subTestSet.issubset(tablecols):
            for lostEntry in subTestSet: 
                rawTables[tableType][lostEntry] = "-"
        rawTables[tableType] = rawTables[tableType][transTablecols]

        mappables_list = list(mappables[tableType].keys())

        for mapping in mappables_list:
            for feature in mappables[tableType][mapping]:
                for i in range(gameTableLength[tableType]):
                    rawTables[tableType].loc[i, feature] = mapId(rawTables[tableType].loc[i, feature], mapping, read_patch)


        rawTables[tableType] = rawTables[tableType].rename(translateDict[tableType], axis="columns")


        # aggregate further
        match tableType:

            case GameTable.META:
                rawTables[tableType].loc[0,"date"] = rawTables[tableType].loc[0,"date"][0:10]

            case GameTable.TEAM:
                for i in range(2):
                    rawTables[tableType].loc[i,"win"] = True if (rawTables[tableType].loc[i,"win"] == "Win") else False

            case GameTable.PLAYER:
                for i in range(10):
                    rawTables[tableType].loc[i,"team"] = playerTeamCheck(rawTables[tableType].loc[i,"team"])

