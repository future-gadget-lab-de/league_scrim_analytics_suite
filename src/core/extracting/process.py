import pandas as pd
from src.core.extracting.client import ClientKeys
from src.core.extracting.matchv5 import MatchV5Keys
from src.core.extracting.scheme import GameData, importPipeline, needsAgg, classify

def dropListEntries(dataframe: pd.DataFrame) -> pd.DataFrame:
    """this method drops all columns of a dataframe, that contain a list.
    
    Parameters
    ----------
    dataframe : pd.DataFrame
        a dataframe to format
        
    Returns
    -------
    dataframe : pd.DataFrame
        the resulting dataframe with dropped lists
        
    """

    list_cols = [c for c in dataframe.columns if dataframe[c].apply(lambda x: isinstance(x, list)).any()]
    return dataframe.drop(columns=list_cols)


def indexByOneVariable(df: pd.DataFrame, var: str) -> pd.DataFrame:
    """this method uses one variable/feature and sets it as the new index variable.

    Parameters
    ----------
    df : pd.DataFrame
        the dataframe, to change
    var : str
        the name of the feature/variable

    Returns
    -------
    dataframe : pd.DataFrame
        the new dataframe indexed by var
    
    """
    dataframe = df.copy()
    colsWithoutMetaKey = list(dataframe.columns).remove(var)
    dataframe["cc"] = dataframe.groupby(var).cumcount()

    indexed_df = dataframe.set_index([var, "cc"])[colsWithoutMetaKey].unstack("cc")
    indexed_df.columns = [f"{a}_{b}" for a, b in indexed_df.columns]
    indexed_df.index = list(range(len(indexed_df.index)))

    return indexed_df


def getData(
    data:    dict, 
    pathKey: MatchV5Keys | ClientKeys = ClientKeys.META, 
    metaKey: list[list[str]] | None = None,
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
    
    if metaKey is not None:
        return indexByOneVariable(listlessDf, "_".join(metaKey[0]))
        
    return listlessDf


def mergeTables(tables: list[pd.DataFrame]) -> pd.DataFrame:
    """merges tables along the rows"""

    dataset = tables.copy()
    for i in range(len(dataset) - 1):
        dataset[0] = dataset[0].join(dataset[i+1])
    
    return dataset[0]


def extractTables(data: dict, pipe: importPipeline) -> dict[str, pd.DataFrame]:
    """Collects all member of a enum class (see head of this file) and 
    executes these onto a data dict, to extract the data and format it into
    three outcomes: PLAYER-, META- and TEAMDATA
    
    Parameters
    ----------
    data : dict
        the raw data, extracted from a .json gamefile
    className : importPipeline
        one of the two classnames above
        
    Returns
    -------
    dataframes : list[pd.DataFrame]
        contains the three major tables: metadata, playerdata, teamdata
        
    """

    METADATA: list[pd.DataFrame]   = []
    PLAYERDATA: list[pd.DataFrame] = []
    TEAMDATA: list[pd.DataFrame]   = []

    for member in pipe:

        metaKey = None
        if member in needsAgg:
            metaKey: list[list[str]] = [needsAgg[member]]

        table: pd.DataFrame = getData(
                data=data,
                pathKey=member,
                metaKey=metaKey
        )

        match classify(member):
            case GameData.TEAM:
                TEAMDATA.append(table)
            case GameData.PLAYER:
                PLAYERDATA.append(table)
            case GameData.META:
                METADATA.append(table)

    return {
        GameData.META:   mergeTables(METADATA), 
        GameData.TEAM:   mergeTables(TEAMDATA), 
        GameData.PLAYER: mergeTables(PLAYERDATA)
    }
