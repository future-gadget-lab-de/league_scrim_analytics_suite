import os

def findMatchFile():
    """
    Finds the first file in the gamefiles/matchdata folder.
    ----------
    Return
    ----------
        matchfile (str):          relative path for the matchfile
    ----------
    """
    filename = os.listdir("gamefiles/matchdata")[0]
    matchfile = "gamefiles/matchdata/"+filename
    return matchfile