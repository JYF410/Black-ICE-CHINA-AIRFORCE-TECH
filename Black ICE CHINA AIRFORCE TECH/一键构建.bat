@echo off
cd /d "%~dp0"
set "PY=C:\Users\JYF\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"

echo ============================================
echo  Chinese Airforce Tech Tree - Build
echo ============================================
echo.

"%PY%" _tools\build\make.py all
if errorlevel 1 goto fail

"%PY%" _tools\package_diag.py
if errorlevel 1 goto fail

echo.
echo BUILD OK.
echo Output: _install\update_game_files.zip
echo.
echo Copy/extract it over:
echo   D:\Steam\steamapps\workshop\content\394360\3844078670
echo (or republish in the launcher)
goto end

:fail
echo.
echo BUILD FAILED - please send the errors above.

:end
echo.
pause
