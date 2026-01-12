# How to install and use plugins

## Prerequisites

If we talk about plugins, it means in literal sense, that you can customize plot routines
based on fixed SQL files and a short python script (in order to define the plot).

There are sample files provided in our repository. If you encounter errors, don't hesitate
to look into our examples.

The support is experimental and only tested under Debian 13.

## Structure

This plugin structure is partitioned into two parts

1. free expansion of custom plots (based on pandas & matplotlib)
2. execution of routines, through a predefined .json file structure

## Plot Expansion:

To expand `lsas` plot codebase you have to drop a **python file**, into `templates/plugins` (relative to the executable), which consists of

1. Three **constant** members, namely
    - `input_layout_c` - which identifies, which kind of dataframes your function can handle.
    ```python
    # For Example:
    # one of the simplest layouts --> one dataframe with a integer row
    input_layout_c = [("int64",)] 
    # more complex examples:
    input_layout_c = [("int64","int64")] # -> one dataframe with 2 integer rows
    input_layout_c = [("int64",), ("int64",)] # two dataframes with 1 integer row
    ```
    - `accept_less_c` - which identifies, if the input layout is still applicable, if you drop
        a number of entries of it.
    ```python
    # assume
    accept_less_c = True
    input_layout_c = [("int64",), ("int64",)] # two dataframes with 1 integer row
    # in this example your method would also be applicable to one dataframe with 1 integer row
    ```
    - `location_c` - which identifies the location where you want to save the file.
    ```python
    # For Example:
    location_c = "graphs/mygraph.png" # --> .../lsas/graphs/mygraph.png
    ```

2. A plot function, which you can freely write, but should satisfie anyway:
    - having `data: list[pd.DataFrame]` as the first positional argument and apart from the first
    only optional ones.
    - the plotfunction should save the file as a `.png` in the specified file location `location_c`
    ```python
    # For Example
    def plot(data: list[pd.DataFrame], somearg = 0) -> None:
        ...

        
        plt.savefig(location_c) # save file under location_c
    ```
3. A optional aggregate function, which only takes only `data: list[pd.DataFrame]` as an argument and also
returns a value with the type `data: list[pd.DataFrame]` (in practise, the aggregatefunction gets chained in between the initial dataframe and the plot function)


## Json Routines:

One can write `.json` files and load them with `./main -p [path/to/template.json]`. The file has to have the structure:

```json
{
    "modulenames": {
        "[name of a .py plugin without the '.py' suffix]": {
            "[optional arg1 of plot]": "[value of arg1]",
            ...
            "[optional argn of plot]": "[value of argn]"
        },
        ...
        "[name of a .py plugin without the '.py' suffix]": {
            "[optional arg1 of plot]": "[value of arg1]",
            ...
            "[optional argn of plot]": "[value of argn]"
        }
    },
    "SQL_files_location": [
        "[path to a .SQL select file]",
        ...
        "[path to a .SQL select file]"
    ]
}

```
The expected behaviour is, that (in pseudo)
```
load the outcome of all SELECT queries into a list of dataframes

for each module in modulenames:
    if aggregate_function exists:
        aggregate the list of dataframes for this module
    
    plot the resulting list of dataframes

```
you plot the dataframes, which result of the queries, for each specified modulename.



