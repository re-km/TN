@echo off
cd /d "%~dp0"

:: 埋め込みPythonがあるか確認
if exist "python\python.exe" (
    :: 埋め込みPythonで起動
    start "" "python\python.exe" "Launcher.py"
) else (
    :: システムのPythonで起動
    start "" python "Launcher.py"
)
