@echo off
echo Building Godot Navmesh Converter with PyInstaller
echo ============================================

REM Set the script name
SET SCRIPT_NAME=godot_navmesh_converter.py

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller is not installed. Installing now...
    pip install pyinstaller
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install PyInstaller. Please install it manually with:
        echo pip install pyinstaller
        pause
        exit /b 1
    )
)

REM Build the executable with icon
echo Building executable...
pyinstaller --onefile --noconsole --icon=icon.ico --name GodotNavmeshConverter --distpath "%CD%\dist" "%SCRIPT_NAME%"

echo.
echo Build completed!
echo The executable is located in the "dist" folder.
echo.

REM Ask if the user wants to set up file associations
set /p SETUP_ASSOC=Do you want to set up file associations for .obj and .tres files? (Y/N): 
if /i "%SETUP_ASSOC%"=="Y" (
    echo.
    echo Setting up file associations...
    
    SET CONVERTER_PATH=%CD%\dist\GodotNavmeshConverter.exe
    echo Executable path: %CONVERTER_PATH%
    
    REM Create file type registrations
    REG ADD "HKEY_CURRENT_USER\Software\Classes\.obj\OpenWithProgids" /v "GodotNavmeshConverter.Document" /t REG_SZ /d "" /f
    REG ADD "HKEY_CURRENT_USER\Software\Classes\.tres\OpenWithProgids" /v "GodotNavmeshConverter.Document" /t REG_SZ /d "" /f
    
    REM Create application registration
    REG ADD "HKEY_CURRENT_USER\Software\Classes\GodotNavmeshConverter.Document" /v "" /t REG_SZ /d "Godot Navmesh File" /f
    REG ADD "HKEY_CURRENT_USER\Software\Classes\GodotNavmeshConverter.Document\DefaultIcon" /v "" /t REG_SZ /d "\"%CONVERTER_PATH%\"" /f
    REG ADD "HKEY_CURRENT_USER\Software\Classes\GodotNavmeshConverter.Document\shell\open\command" /v "" /t REG_SZ /d "\"%CONVERTER_PATH%\" \"%%1\"" /f
    
    REM Add to "Open with" menu
    REG ADD "HKEY_CURRENT_USER\Software\Classes\Applications\GodotNavmeshConverter.exe\shell\open\command" /v "" /t REG_SZ /d "\"%CONVERTER_PATH%\" \"%%1\"" /f
    
    echo File associations set up successfully!
)

echo.
echo All done! Your GodotNavmeshConverter.exe is ready to use.
echo You can now convert between .obj and .tres files by:
echo 1. Dragging and dropping files onto the executable
echo 2. Double-clicking on files (if you set up file associations)
echo 3. Running from command line: GodotNavmeshConverter.exe input_file [output_file]
pause