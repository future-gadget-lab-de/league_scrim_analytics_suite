"""This file contains code for reformatting raw data"""
import pandas as pd

def listOfDictsToDF(data: list[dict]) -> pd.DataFrame:
    """changes a singlerow dict format into a DataFrame

    Parameters
    ----------
    data : list[dict]
        data in the form, where each entry of the list is a dict
        where 'feature -> value' is mapped

    Returns
    -------
    data : pd.DataFrame
        the data in the dataframe format
    
    """
    if len(data) == 0:
        return pd.DataFrame()
    finaldict = dict()

    for key in data[0].keys():
        list_of_values = list()
        for dict_ in data:
            list_of_values.append(dict_[key])
        finaldict[key] = list_of_values

    return pd.DataFrame.from_dict(finaldict)