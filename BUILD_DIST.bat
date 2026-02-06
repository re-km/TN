@echo off
setlocal
chcp 65001

echo ========================================================
echo  Tunnel Tools Distribution Builder
echo ========================================================
echo.

set "DIST_DIR=dist_package"

if exist "%DIST_DIR%" (
    echo [INFO] Removing existing dist directory...
    rmdir /s /q "%DIST_DIR%"
)
mkdir "%DIST_DIR%"

echo [INFO] Copying tools...
xcopy /E /I /Y "DXF_facility_counter" "%DIST_DIR%\DXF_facility_counter"
xcopy /E /I /Y "Crack_Density" "%DIST_DIR%\Crack_Density"
xcopy /E /I /Y "D-1-1_2InputSheet" "%DIST_DIR%\D-1-1_2InputSheet"
xcopy /E /I /Y "D-3_sheet_creater" "%DIST_DIR%\D-3_sheet_creater"
xcopy /E /I /Y "DXF2D-2" "%DIST_DIR%\DXF2D-2"
xcopy /E /I /Y "paint4save" "%DIST_DIR%\paint4save"

echo [INFO] Copying Launcher and Config...
copy /Y "Launcher.py" "%DIST_DIR%\"
copy /Y "tools.json" "%DIST_DIR%\"
copy /Y "Manual.html" "%DIST_DIR%\"
copy /Y "Launcher.bat" "%DIST_DIR%\"
copy /Y "requirements.txt" "%DIST_DIR%\"

echo.
echo [IMPORTANT]
echo Distribution package created in "%DIST_DIR%".
echo To make it standalone:
echo 1. Download Python Embeddable Package (e.g. 3.11).
echo 2. Extract it to "%DIST_DIR%\python".
echo 3. Install dependencies:
echo    "%DIST_DIR%\python\python.exe" -m pip install -r "%DIST_DIR%\requirements.txt"
echo.
pause
