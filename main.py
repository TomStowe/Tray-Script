from infi.systray import SysTrayIcon
import os, sys
from src.Options import Options
from os.path import exists, splitext

##### Config #####
timeoutSeconds = 60
settingsFilePath = "settings.json"
##### Config #####
    
def resetProgram():
    os.execl(sys.executable, sys.executable, *sys.argv)
    
options = Options(resetProgram)

def addCommandsToTuple(commands, tuple):
    for command in commands:
        icon = command.icon
        if (command.icon == "" or command.icon == None):
            icon = None
        else:
            _, extension = splitext(command.icon)
            
            # Ensure that the icon is valid
            if (not(exists(command.icon) and extension == ".ico")):
                icon = None
            
        # Recursively add items if a command list
        if (command.commandList != None):
            tuple = tuple + ((command.name, icon, addCommandsToTuple(command.commandList, ())),)
                
        else:
            tuple = tuple + (((
                command.name,
                icon,
                command.getActionableCommand())),
            )
    return tuple
        
# Convert the command list to a tuple list
updatedCommands = ()
updatedCommands = addCommandsToTuple(options.commands, updatedCommands)

# Add the options page if there are no nested commands
updatedCommands = updatedCommands + ((("Options", "icons/settings.ico", options.showOptionsPage)),)

sysTrayIcon = SysTrayIcon("icons/main.ico", "Tray Script", updatedCommands, default_menu_index=len(updatedCommands)-1)
sysTrayIcon.start()