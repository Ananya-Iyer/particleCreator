# particleCreator
A fun plugin to attach particles on the mesh and to apply dynamics on it


How to run?

import maya.cmds as cmds

1. Create a sphere
2. load the plugin
    1. Windows >> Settings/Preferences >> Plugin Manager >> (load the plugin)
    or
    2. cmds.loadPlugin(pathToPlugin.py)
3. cmds.particleCreator(sparse=True)
