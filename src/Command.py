import os

"""
    Runs a specific command from this app
    command: The command to run
"""
def runCommand(command:str):
    os.system("cmd /c " + command)
    
"""
    Defines the command datatype
"""
class Command:
    """
        The constructor for the Command datatype
        name: The name of the command
        command: The command to perform
        icon: The icon to use
    """
    def __init__(self, name, command, icon=None):
        self.name = name
        self.command = command
        self.icon = icon
        
    """
        Converts the object into a dictionary
        Returns: The dictionary representation of the object
    """
    def __dict__(self):
        outDict = {
            "name": self.name,
            "command": self.command
        }
        if (self.icon != None):
            outDict["icon"] = self.icon
        
        return outDict
        
    """
        Creates the actionable command
    """
    def getActionableCommand(self):
        return lambda x: runCommand(self.command)