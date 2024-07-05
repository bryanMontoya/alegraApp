@echo off
echo Welcome to AlegraApp!

::Function to check if the internet connection is active
:CheckConnection
echo Checking internet connection...
ping www.google.com -n 1 >nul
if %errorlevel%==0 (
    echo Internet connection is active.
    goto :CheckPython
) else (
    echo Please connect to internet. 
    goto :End
)


:: Function to check if the specific Python version is installed
:CheckPython
python --version 2>&1 | find "3.9.13" >nul
if %errorlevel%==0 (
    echo Python 3.9.13 is already installed.
    goto :InstallPackages
) else (
    echo Python 3.9.13 is not installed.
    goto :InstallPython
)

:: Function to install Python
:InstallPython
echo Downloading and installing Python 3.9.13...
bitsadmin /transfer "PythonDownload" https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe %TEMP%\python-3.9.13-amd64.exe
start /wait %TEMP%\python-3.9.13-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
if %errorlevel%==0 (
    echo Python 3.9.13 has been successfully installed.
) else (
    echo Failed to install Python 3.9.13. Exiting.
    goto :End
)

::Function to install the required Python packages
:InstallPackages
echo Installing required Python packages...
pip install -r requirements.txt >nul 2>&1
if %errorlevel%==0 (
    echo Required Python packages have been successfully installed.
    goto :RunScript
) else (
    echo Failed to install required Python packages. Exiting.
    goto :End
)

::Function to run the Python script
:RunScript
python app/app.py
if %errorlevel%==0 (
    echo Python script has been successfully executed.
    goto :End
) else (
    echo Failed to execute Python script. Exiting.
    goto :End
)

::Start Process
call :CheckConnection

::End Process
:End

echo Ending AlegraApp.
echo Bye Bye
pause
