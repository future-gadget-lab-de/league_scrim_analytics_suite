import os
import pandas as pd
import matplotlib.pyplot as plt

# this file accepts a maximum of two dataframes, with one col each:
# --> because we stored two tuples with a int entry each and accept_less_c is true (we allow less than two)
input_layout_c = [("int64",),("int64",)]
accept_less_c = True
location_c = "gamefiles/test.png"

def simpleHistoLSAS(data: list[pd.DataFrame], color: str = "blue", dim: tuple[int,int] = (400,400)) -> None:
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

    dpi = 100
    figsize = (float(dim[0])/float(dpi), float(dim[1])/float(dpi))
    
    plt.figure(dpi, figsize)

    plt.hist(data.iloc[:,0], color=color, edgecolor="black")

    plt.ylabel("test")
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
    