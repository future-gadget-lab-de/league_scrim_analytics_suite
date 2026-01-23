"""file for function manipulation. Methods to use:
- param_names - returns names of args
- chainFunctions - chains passed fucntions
- executeAlongList - executes a function for every list element

"""

from loguru import logger
import inspect

def param_names(fn) -> list[str]:
    """returns the names of a functions parameters as a list of strings
    
    Parameters
    ----------
    fn
        the name of a any python function
    
    Returns
    -------
    arglist : list[str]
        a list with all args of fn

    """
    logger.trace(f"returned the names of the function {fn} arguments.")
    return [p.name for p in inspect.signature(fn).parameters.values()]

def chainFunctions(kwargs: dict, functions: list) -> object:
    """
    chains multiple functions with each other. assumes that the returnvalues of the functionlist
    is equal to the arguments the next function has.

    Parameters
    ----------
    kwargs : dict
        the kwargs, used for the first function in the list
    functions : list[function]
        a list of any function
    
    Returns
    -------
    returnValue : object
        the return of the last function
    

    """

    returnValue = functions[0](**kwargs)
    functions.pop(0)

    for func in functions:
        kwarg_names = param_names(func)
        if len(kwarg_names) == 1:
            kwarg = { kwarg_names[0]: returnValue }
        else:
            kwarg = { kwarg_names[i]: returnValue[i] for i, _ in enumerate(kwarg_names) }

        returnValue = func(**kwarg)

    return returnValue


def executeAlongList(kwargslist: list[dict], function) -> list:
    """
    Executes a function for every element in the passed list.

    Parameters
    ----------
    kwargslist : list[dict]
        a list of kwargs, which are executed onto the passed function
    function : function
        any function 

    Returns
    -------
    returns : list
        a list of every return per arg in kwargslist
    
    """
    returns: list = []

    for kwargs in kwargslist:

        returns.append(function(**kwargs))

    return returns