import os, subprocess, threading

"""
    Runs a specific command from this app
    command: The command to run
    runInBackground: Whether the command should be run in the background
"""
def runCommand(command:str, runInBackground: bool):
    thread = threading.Thread(target=__runCommand, args=(command, runInBackground,))
    thread.start()
    
"""
    The private method to run a specific command
    command: The command to run
    runInBackground: Whether the command should be run in the background
"""
def __runCommand(command: str, runInBackground: bool):
    if (not runInBackground):
        os.system("cmd /c " + command)
    else:
        subprocess.Popen(command, shell=True)
    
"""
    Defines the command datatype
"""
class Command:
    """
        The constructor for the Command datatype
        name: The name of the command
        command: The command to perform
        commandList: The list of commands nested in the command
        runCommandInBackground: Whether to run the command in the background
        icon: The icon to use
    """
    def __init__(self, name, command, commandList, runCommandInBackground, icon=None):
        self.name = name
        self.command = command
        self.commandList = commandList
        self.runCommandInBackground = runCommandInBackground
        self.icon = icon
        
    """
        Converts the object into a dictionary
        Returns: The dictionary representation of the object
    """
    def __dict__(self):
        outDict = {
            "name": self.name,
            "runCommandInBackground": self.runCommandInBackground
        }
        if (self.commandList != None and len(self.commandList) != 0):
            outDict["commandList"] = self.commandList
        else:
            outDict["command"] = self.command
        
        if (self.icon != None):
            outDict["icon"] = self.icon
        
        return outDict
        
    """
        Creates the actionable command
    """
    def getActionableCommand(self):
        return lambda x: runCommand(self.command, self.runCommandInBackground)