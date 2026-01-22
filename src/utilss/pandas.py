import pandas as pd

def mergeTables(tables: list[pd.DataFrame]) -> pd.DataFrame:
    """merges tables along the rows, but assumes unique colnames!"""

    dataset = tables.copy()
    for i in range(len(dataset) - 1):
        dataset[0] = dataset[0].join(dataset[i+1], rsuffix="_other")
    
    return dataset[0]


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
    colsWithoutMetaKey = list(dataframe.columns)
    colsWithoutMetaKey.remove(var)
    dataframe["cc"] = dataframe.groupby(var).cumcount()

    indexed_df = dataframe.set_index([var, "cc"])[colsWithoutMetaKey].unstack("cc")
    indexed_df.columns = [f"{a}_{b}" for a, b in indexed_df.columns]
    indexed_df.index = list(range(len(indexed_df.index)))

    return indexed_df