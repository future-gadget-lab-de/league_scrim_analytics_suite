"""helper methods for manipulation pandas dataframes. i.e.
- merging tables
- drop list entries
- index by a certain feature
"""
from loguru import logger
import pandas as pd
import numpy as np

def mergeTables(tables: list[pd.DataFrame]) -> pd.DataFrame:
    """merges tables along the rows, but assumes unique colnames!"""
    logger.trace("Starting merging dataframes with each other.")
    if not tables:
        return pd.DataFrame()
    dataset = tables.copy()
    for i in range(len(dataset) - 1):
        dataset[0] = dataset[0].join(dataset[i+1], rsuffix="_other")
    
    return dataset[0]

def concatOnPrefixes(table: pd.DataFrame, prefixes: list[str], ident: str) -> pd.DataFrame:
    """Partition columns by prefix and stack matches row-wise.

    For each prefix in prefixes:
      - take all columns starting with the prefix
      - append all non-matching columns
      - add a column 'ident' with the prefix label
    Then concatenate these partitions along rows.
    """
    if table is None or table.empty:
        return pd.DataFrame()
    if not prefixes:
        result = table.copy()
        return result

    cols = list(table.columns)
    nonmatch_cols = [c for c in cols if not any(c.startswith(p) for p in prefixes)]

    parts: list[pd.DataFrame] = []
    for p in prefixes:
        match_cols = [c for c in cols if c.startswith(p)]
        if not match_cols:
            continue
        part = pd.concat([table[match_cols], table[nonmatch_cols]], axis=1)
        part = part.copy()

        part.columns = [s.removeprefix(p) for s in part.columns]
        
        parts.append(part)

    if not parts:
        result = table[nonmatch_cols].copy()
        return result

    res = pd.concat(parts, axis=0, ignore_index=True)
    #res.columns = 

    return res
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
    logger.trace("dropped List entries of a dataframe.")
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
    logger.trace(f"Starting index a dataframe via the feature {var}.")
    dataframe = df.copy()
    colsWithoutMetaKey = list(dataframe.columns)
    colsWithoutMetaKey.remove(var)
    dataframe["cc"] = dataframe.groupby(var).cumcount()

    indexed_df = dataframe.set_index([var, "cc"])[colsWithoutMetaKey].unstack("cc")
    indexed_df.columns = [f"{a}_{b}" for a, b in indexed_df.columns]
    indexed_df.index = list(range(len(indexed_df.index)))

    return indexed_df
