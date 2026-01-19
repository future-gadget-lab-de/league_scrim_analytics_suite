import os
import pandas as pd
import matplotlib.pyplot as plt

# list of tuples, where each listmember is a seperate table
# and each entry in a tuple the "columntype" of a column
input_layout_c = [("int64",)]

# is this file accepting less tables, than specified?
accept_less_c = False

# where the file is saved
location_c = "gamefiles/test.png"

def simpleHistoLSAS(data: list[pd.DataFrame], color = "blue", dim = (400,400)) -> None:
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
