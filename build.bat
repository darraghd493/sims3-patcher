@echo off

title sims3-patcher Builder (using pyinstaller)
echo sims3-patcher Builder (using pyinstaller)
echo.

echo Downloading pyinstaller...
pip3 install pyinstaller>pyinstaller.log
echo.

echo Building...
del sims3-patcher.spec>pyinstaller.log
pyinstaller --onefile --noconsole --icon=sims3-patcher.ico main.py>pyinstaller.log

echo Cleaning...
del sims3-patcher.spec>pyinstaller.log
echo.

echo.
echo Done!
echo.

echo Do you want to delete the log file?
echo.
echo [1] Yes
echo [2] No
echo.

set /p choice=Choice: 
if %choice%==1 goto delete
if %choice%==2 goto exit

:delete
del pyinstaller.log
echo.
echo Done!
echo.

:exit
echo Press any key to exit...
pause>nul
exit
