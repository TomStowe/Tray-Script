import tkinter as tk
from tkinter import ttk
from src.ConfigReader import loadSettings, saveSettings
from src.Command import Command, runCommand
import threading
from os.path import exists, splitext

selectedOptionName = None

class Options:
    settingsLocation = "settings.json"
    commands = []
    
    resetTrayFunction = None
    
    selectedIndex = 0
    selectedCommandNameField = None
    selectedCommandField = None
    selectedIconField = None
    
    """
        Constructor for the options menu
        resetTrayFunction: The function to be called to reset the tray
    """
    def __init__(self, resetTrayFunction):
        # Load the settings if they are available
        self.commands = loadSettings(self.settingsLocation)
        self.resetTrayFunction = resetTrayFunction
    
    """
        Function for creating the options page
        NA: Useless param that is required by the tray icon library
    """
    def showOptionsPage(self, NA):
        # root window
        self.root = tk.Tk()
        self.root.title("Tray Command Options")
        self.root.attributes('-topmost', 1)
        self.root.iconbitmap('./icons/main.ico')
        self.root.geometry('600x400+50+50')
        self.root.resizable(False, False)
        # windows only (remove the minimize/maximize button)
        self.root.attributes('-toolwindow', True)
        self.root.protocol("WM_DELETE_WINDOW", self.resetTrayFunction)

        # layout on the root window
        self.root.columnconfigure(0, weight=2)
        self.root.columnconfigure(1, weight=3)

        self.listFrame = self.__createListFrame(self.root)
        self.listFrame.grid(column=0, row=0)

        self.inputFrame = self.__createInputFrame(self.root)
        self.inputFrame.grid(column=1, row=0)
        self.__toggleItemSelected(False)

        self.root.mainloop()
        
    """
        Creates the frame for collecting user input for the command details
        container: The container that the frame should be added to
    """
    def __createInputFrame(self, container):
        frame = ttk.Frame(container)

        # grid layout for the input frame
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(0, weight=3)

        # The name of the command
        ttk.Label(frame, text='Command Name:').grid(column=0, row=0, sticky=tk.W)
        self.selectedCommandNameField = tk.Text(frame, width=27, height=1)
        self.selectedCommandNameField.focus()
        self.selectedCommandNameField.grid(column=1, row=0, sticky=tk.W)

        # The command itself
        ttk.Label(frame, text='Command:').grid(column=0, row=1, sticky=tk.W)
        self.selectedCommandField = tk.Text(frame, width=27, height=10)
        self.selectedCommandField.grid(column=1, row=1, sticky=tk.W)

        # The icon
        ttk.Label(frame, text='Path To Icon: (.ico files only').grid(column=0, row=2, sticky=tk.W)
        self.selectedIconField = tk.Text(frame, width=27, height=1)
        self.selectedIconField.grid(column=1, row=2, sticky=tk.W)
        
        # Error Text
        self.errorText = tk.StringVar()
        self.errorText.set("")
        self.errorLabel = ttk.Label(frame, textvariable=self.errorText)
        self.errorLabel.configure(foreground="red")
        self.errorLabel.grid(column=0, columnspan=4, row=3)
        
        # Buttons
        buttonWidth = 25
        self.addNewCommandButton = ttk.Button(frame, text="Add New Command", command=self.__addNewCommand, width=buttonWidth)
        self.addNewCommandButton.grid(column=0, row=4, sticky=tk.W)
        self.updateSelectedButton = ttk.Button(frame, text="Update Selected Command", command=self.__updateCommand, width=buttonWidth)
        self.updateSelectedButton.grid(column=1, row=4, sticky=tk.W)
        self.deleteSelectedButton = ttk.Button(frame, text="Test Command", command=self.__testCommand, width=buttonWidth)
        self.deleteSelectedButton.grid(column=0, row=5, sticky=tk.W)
        self.deleteSelectedButton = ttk.Button(frame, text="Delete Command", command=self.__deleteCommand, width=buttonWidth)
        self.deleteSelectedButton.grid(column=1, row=5, sticky=tk.W)

        for widget in frame.winfo_children():
            widget.grid(padx=0, pady=5)

        return frame

    """
        Create the frame containing the list of commands created
        container: The container used to store the frame
    """
    def __createListFrame(self, container):
        frame = ttk.Frame(container)

        frame.columnconfigure(0, weight=1)
        
        self.listBoxData = tk.StringVar(value=tuple(map(lambda x: x.name, self.commands)))
        
        self.listBox = tk.Listbox(frame, height=22, width=30, listvariable=self.listBoxData, selectmode=tk.SINGLE)
        scrollbar = ttk.Scrollbar(
        frame,
        orient='vertical',
        command=self.listBox.yview
        )
        
        self.listBox.grid(
        column=0,
        columnspan=2,
        row=0,
        sticky='nwes'
        )

        self.listBox['yscrollcommand'] = scrollbar.set

        scrollbar.grid(
            column=2,
            row=0,
            sticky='ns')
        
        self.upButton = ttk.Button(frame, text="^", width=4, command=self.__moveItemUpInList)
        self.upButton.grid(column=0, row=1, sticky="e")
        self.downButton = ttk.Button(frame, text="v", width=4, command=self.__moveItemDownInList)
        self.downButton.grid(column=1, row=1, sticky="w")
        
        """
            The function used to get the selected command from the list
        """
        def items_selected(event):
            """ handle item selected event
            """
            # get selected indices
            if (len(self.listBox.curselection()) == 0):
                return
            
            selectedCommand = self.commands[self.listBox.curselection()[0]]
            self.selectedIndex = self.listBox.curselection()[0]
            self.selectedCommandNameField.delete(1.0, "end")
            self.selectedCommandNameField.insert(1.0, selectedCommand.name)
            self.selectedCommandField.delete(1.0, "end")
            self.selectedCommandField.insert(1.0, selectedCommand.command)
            self.selectedIconField.delete(1.0, "end")
            self.selectedIconField.insert(1.0, selectedCommand.icon)
            self.__toggleItemSelected(True)
            
        self.listBox.bind('<<ListboxSelect>>', items_selected)

        for widget in frame.winfo_children():
            widget.grid(padx=0, pady=3)

        return frame
    
    """
        Updates all of the UI elements when an item is selected in the listbox
    """
    def __toggleItemSelected(self, isSelected):
        if (isSelected):
            self.upButton["state"] = "normal"
            self.downButton["state"] = "normal"
            self.updateSelectedButton["state"] = "normal"
            self.deleteSelectedButton["state"] = "normal"
        else:
            self.upButton["state"] = "disabled"
            self.downButton["state"] = "disabled"
            self.updateSelectedButton["state"] = "disabled"
            self.deleteSelectedButton["state"] = "disabled"
            self.errorText.set("")

    """
        The function used to add a new command to the config
    """
    def __addNewCommand(self):
        command = self.__getCommandFromTextInputs()
        
        if (command == None):
            return
        
        self.commands.append(command)
        
        self.__updateStoredSettings()
        
    """
        The function used to update the data stored in a command
    """
    def __updateCommand(self):
        command = self.__getCommandFromTextInputs()
        
        if (command == None or self.selectedIndex == None or self.selectedIndex > len(self.commands)):
            return
        
        self.commands[self.selectedIndex] = command
        
        self.__updateStoredSettings()
        
    """
        The function used to test the command input
    """
    def __testCommand(self):
        command = self.__getCommandFromTextInputs()
        
        if (command == None or self.selectedIndex == None or self.selectedIndex > len(self.commands)):
            self.errorText.set("Could not test the command.\nPlease ensure that the name and command box are filled in")
            return
        else:
            self.errorText.set("")
        
        thread = threading.Thread(target=runCommand, args=(command.command,))
        thread.start()
        #runCommand(command.command)
        
    """
        The function used to delete the command
    """
    def __deleteCommand(self):
        if (self.selectedIndex == None or self.selectedIndex > len(self.commands)):
            self.errorText.set("Could not a delete this command.\nPlease click on the item and try again")
            return
        
        self.commands.pop(self.selectedIndex)
        
        self.__updateStoredSettings()
        
    """
        The function used to get the command from the text inputs
        returns: The generated command
    """
    def __getCommandFromTextInputs(self):
        commandName = self.selectedCommandNameField.get(1.0, "end").rstrip("\n")
        command = self.selectedCommandField.get(1.0, "end").rstrip("\n")
        icon = self.selectedIconField.get(1.0, "end").rstrip("\n")
        
        if (commandName == None or commandName == "" or command == None or command == ""):
            self.errorText.set("Please ensure the name and command box are filled in")
            return None
        
        if (icon == ""):
            icon = None
        else:
            _, extension = splitext(icon)
            if (not(exists(icon) and extension == ".ico")):
                self.errorText.set("Please ensure that the icon exists and is an ico file")
                return
        
        return Command(commandName, command, icon)
        
    """
        A function to update the settings stored in the settings file and updates the options window
        resetWindow: Whether the window should be updated, defaults to true
    """
    def __updateStoredSettings(self, resetWindow=True):
        saveSettings(self.settingsLocation, self.commands)
        
        # Reset the windows
        if (resetWindow):
            self.inputFrame.destroy()
            self.inputFrame = self.__createInputFrame(self.root)
            self.inputFrame.grid(column=1, row=0)
            self.listFrame.destroy()
            self.listFrame = self.__createListFrame(self.root)
            self.listFrame.grid(column=0, row=0)
            self.__toggleItemSelected(False)
            self.root.update()
    
    def __moveItemUpInList(self):
        # We can't move the item up higher than the top
        if (self.selectedIndex == 0):
            return
        
        # Swap the data over on the UI
        listBoxDataList = self.__getListBoxData()
        move = listBoxDataList[self.selectedIndex]
        listBoxDataList.pop(self.selectedIndex)
        listBoxDataList.insert(self.selectedIndex-1, move)
        self.listBoxData.set(tuple(listBoxDataList))
        self.listBox.select_clear(self.selectedIndex)
        self.listBox.select_set(self.selectedIndex-1)
        
        # Swap over the data in the stored commands
        move = self.commands[self.selectedIndex]
        self.commands.pop(self.selectedIndex)
        self.commands.insert(self.selectedIndex-1, move)
        self.__updateStoredSettings(False)
        
        # Update the selected index stored
        self.selectedIndex = self.selectedIndex - 1
    
    def __moveItemDownInList(self):
        # We can't move the item up lower than the bottom
        if (self.selectedIndex >= len(self.commands)):
            return
        
        # Swap the data over on the UI
        listBoxDataList = self.__getListBoxData()
        move = listBoxDataList[self.selectedIndex]
        listBoxDataList.pop(self.selectedIndex)
        listBoxDataList.insert(self.selectedIndex+1, move)
        self.listBoxData.set(tuple(listBoxDataList))
        self.listBox.select_clear(self.selectedIndex)
        self.listBox.select_set(self.selectedIndex+1)
        
        # Swap over the data in the stored commands
        move = self.commands[self.selectedIndex]
        self.commands.pop(self.selectedIndex)
        self.commands.insert(self.selectedIndex+1, move)
        self.__updateStoredSettings(False)
        
        # Update the selected index stored
        self.selectedIndex = self.selectedIndex + 1
    
    def __getListBoxData(self):
        return self.listBoxData.get().replace("'", "").replace("(", "").replace(")", "").split(", ")
        


