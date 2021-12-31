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
    """
    def __init__(self, name, command):
        self.name = name
        self.command = command
        
    """
        Converts the object into a dictionary
        Returns: The dictionary representation of the object
    """
    def __dict__(self):
        return {
            "name": self.name,
            "command": self.command
        }
        
    """
        Creates the actionable command
    """
    def getActionableCommand(self):
        return lambda x: runCommand(self.command)