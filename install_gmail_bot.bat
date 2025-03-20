@echo off
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not found! Installing Python...
    powershell Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe" -OutFile python_installer.exe
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
)
echo Installing Gmail Automation Tool...
pip install --upgrade pip
pip install .
echo Installation Complete! You can now use 'gmail-bot' from the command line.
pause
78