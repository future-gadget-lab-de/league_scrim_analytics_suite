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
    return [p.name for p in inspect.signature(fn).parameters.values()]

def chainFunctions(kwargs: dict, functions: list) -> object:

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

    returns: list = []

    for kwargs in kwargslist:

        returns.append(function(**kwargs))

    return returns