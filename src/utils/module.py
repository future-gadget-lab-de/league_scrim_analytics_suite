from loguru import logger
import importlib.util
import inspect, sys


def iter_defined_members(module) -> list[tuple]:
    """returns a list of all non builtin or imported members of a module
    
    Parameters
    ----------
    module
        any python module
        
    Returns
    -------
    member : list[tuple]
        a list of all members seperated in (nameOfMember,member)
    """

    logger.trace("Started iter_defined_members function with Input:" + str(module) )
    members = list()
    mod = module
    for name, obj in vars(mod).items():
        if name.startswith("_"):
            continue
        if inspect.ismodule(obj):
            continue
        if inspect.isfunction(obj) or inspect.isclass(obj):
            if getattr(obj, "__module__", None) != mod.__name__:
                continue

        members.append((name,obj))
    logger.trace("Finished iter_defined_members function with Output: "+ str(members))
    return members

def import_from_path(module_name: str, file_path: str):
    """imports a specific module by path and name and returns it
    
    Parameters
    ----------
    module_name : str
        the name of the module
    file_path : str
        the path to the named module

    Returns
    -------
    module
        the imported module
    
    """

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module