:: Reset the build folder
if exist build rmdir /s /q build
mkdir build
cd build

:: Run the python build script
python3 -m PyInstaller --name "TrayScript" --hidden-import=pkg_resources --onefile --noconsole --icon ../icons/main.ico ../main.py

:: Copy the required folders
copy ..\settings.json dist\settings.json
echo d | xcopy ..\icons dist\icons

:: Exit out of the build dir
cd ../