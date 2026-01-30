import os
import pandas as pd
import matplotlib.pyplot as plt

# this file accepts a maximum of two dataframes, with one col each:
# --> because we stored two tuples with a int entry each and accept_less_c is true (we allow less than two)
input_layout_c = [("int64",)]
accept_less_c = False
location_c = "gamefiles/test.png"
size_c = (400, 400)

def histoLSAS(data: list[pd.DataFrame], color: str = "blue") -> None:
    """first easy template. this builds a simple histogram
    
    Parameters
    ----------
    data : list[pd.DataFrame]
        the necessary DataFrame parameter
    color : str, optional
        a color
    dim : tuple[int,int], optional
        the dimensions of the diagram in int x int
        
    """

    data = data[0]
    colname = list(data.columns)[0]

    dpi = 90
    figsize = (float(size_c[0])/float(dpi), float(size_c[1])/float(dpi))
    # figsize = size_c
    plt.figure(dpi, figsize)

    plt.hist(data.iloc[:,0], color=color, edgecolor="black")

    plt.ylabel("occurences")
    plt.xlabel(colname)
    plt.grid()
    os.makedirs(os.path.dirname(location_c), exist_ok=True)
    plt.savefig(location_c)
    plt.close()

def simpleAggregateFunction(data_list: list[pd.DataFrame]) -> list[pd.DataFrame]:
    """this is a simple aggregation by just dropping all, except the first dataframe

    Parameters
    ----------
    data_list : list[pd.DataFrame]
        input frame

    Returns
    -------
    data : list[pd.DataFrame]
        aggregated frame
    
    """

    while len(data_list) > 1:
        data_list.pop(-1)

    return data_list
    