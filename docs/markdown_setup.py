import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import src.utils as ut

paths = ut.list_relative_filepaths("docs/source/markdown")

if os.path.isfile("docs/source/order.json"):
    order = ut.loadjsonfiles("docs/source/order.json")

if len(order) != len(paths) + 1:
    raise Exception("order not set, for all files provided")

for i in range(1,len(order)+1):    
    with open("docs/source/index.rst", 'a', encoding="utf-8") as file:
        if order[str(i)].startswith("api"):
            file.write("\n   " + order[str(i)])
            continue
        file.write("\n   markdown/" + order[str(i)])


with open("docs/source/api/modules.rst", encoding="utf-8") as file:
    lines = [line for line in file]  # remove \n
 
lines[0] = lines[0].removeprefix("src")
lines[0] = "API reference"+lines[0]

lines[1] = lines[1].removeprefix("===")

for _ in range(len(lines[0])-1):
    lines[1] = "=" + lines[1]

with open("docs/source/api/modules.rst", 'w', encoding="utf-8") as file:
    for line in lines:
        file.write(line)