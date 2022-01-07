import json, os
from src.Command import Command

"""
    Load the settings from the specified JSON file
    filePath: The specified JSON file to load the settings from
    Returns: The commands
"""
def loadSettings(filePath):
    # Open file
    f = open(os.getcwd() + "\\" + filePath, "r")
    data = json.loads(f.read())
    f.close()
    
    jsonCommands = data.get("commands", None)
    
    if (jsonCommands == None):
        return []
    
    # Get the valid commands
    return __getCommands(jsonCommands)
        
def __getCommands(jsonCommands):
    commands = []
    for jsonCommand in jsonCommands:
        name = jsonCommand.get("name", None)
        command = jsonCommand.get("command", None)
        commandList = jsonCommand.get("commandList", None)
        runCommandInBackground = jsonCommand.get("runCommandInBackground", False)
        icon = jsonCommand.get("icon", None)
        
        if (name != None and (command != None or commandList != None)):
            if (commandList != None and isinstance(commandList, list)):
                commands.append(Command(name, None, __getCommands(commandList), runCommandInBackground, icon))
            else:
                commands.append(Command(name, command, None, runCommandInBackground, icon))
    
    return commands
        
"""
    Save the commands to the settings file
    filePath: The file path to save the settings to
    commands: The list of commands to save to the settings file
"""
def saveSettings(filePath, commands):
    jsonCommands = []
    
    for command in commands:
        jsonCommands.append(command.__dict__())
        
    f = open(os.getcwd() + "\\" + filePath, "w")
    f.write(json.dumps({"commands": jsonCommands}, indent=4))
    f.close()
