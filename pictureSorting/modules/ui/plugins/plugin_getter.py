import importlib
import pkgutil
from pathlib import Path
import re
import inspect

parent_name = '.'.join(__name__.split('.')[:-1])

discovered_plugins = {}

for finder, name, ispkg in pkgutil.iter_modules(path=[str(Path(__file__).parent)]):
    if re.match(r"tab_[0-9]+", name):
        # exclude tab_00
        if name == "tab_00":
            continue
        a = importlib.import_module(".".join([parent_name, name]))
        members = inspect.getmembers(a, inspect.isclass)
        for class_name, class_obj in members:
            if re.match(r"Tab[0-9]+", class_name):
                discovered_plugins[name] = (class_obj)
# print(discovered_plugins)