# Tunnel Inspection Support Tools Launcher (TN)

This repository contains the launcher and distribution scripts for the Tunnel Inspection Support Tools suite.

## Overview
This project provides a centralized launcher (`Launcher.py` / `Launcher.bat`) to manage and execute various standalone tools used for tunnel inspection data processing. It also includes scripts to package the tools for offline distribution.

## Key Files
- **Launcher.py**: The main GUI application (Flet-based) to launch tools.
- **Launcher.bat**: Portable startup script (auto-detects embedded Python).
- **BUILD_DIST.bat**: Script to create a distribution package (`dist_package`) containing the launcher and all tools.
- **tools.json**: Configuration file defining the registered tools.
- **requirements.txt**: Python dependencies for the launcher environment.

## Usage
1. Run `Launcher.bat` to open the tool selection menu.
2. Click "起動" on any tool card to launch that specific tool.

## Distribution
To create a portable package for other PCs:
1. Run `BUILD_DIST.bat`.
2. A `dist_package` folder will be created.
3. Download a standard Python Embeddable Package (zip) and extract it to `dist_package/python`.
4. Install dependencies using `pip` into that embedded Python.
