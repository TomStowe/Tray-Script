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

# Convert the command list to a tuple list
updatedCommands = []
for command in options.commands:
    icon = command.icon
    _, extension = splitext(command.icon)
    
    # Ensure that the icon is valid
    if (not(exists(command.icon) and extension == ".ico")):
        icon = None
        
    updatedCommands.append((
        command.name,
        icon,
        command.getActionableCommand())
    )
    
# Add the options page
updatedCommands.append(("Options", "icons/settings.ico", options.showOptionsPage))

sysTrayIcon = SysTrayIcon("icons/main.ico", "Tray Script", tuple(updatedCommands), default_menu_index=len(updatedCommands)-1)
sysTrayIcon.start()