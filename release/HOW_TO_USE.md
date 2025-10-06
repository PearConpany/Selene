# How to Build and Install Selene on Windows

This guide provides step-by-step instructions to compile the Selene application and create a Windows installer.

## Prerequisites

Before you begin, you need to install the following software on your Windows machine:

1.  **Python:** Download and install the latest version of Python from the [official website](https://www.python.org/downloads/windows/). Make sure to check the box **"Add Python to PATH"** during installation.

2.  **PyInstaller:** This tool packages the Python application into a standalone executable. Open a Command Prompt (cmd) or PowerShell and run the following command:
    ```
    pip install pyinstaller
    ```

3.  **NSIS (Nullsoft Scriptable Install System):** This tool creates the installer. Download and install NSIS from the [official website](https://nsis.sourceforge.io/Download).

## Step 1: Prepare the Icon

The build script requires the application icon to be in the `.ico` format.

1.  The project's logo is located at `Functions/luna/Assets/icono.png`. You need to convert this file to an `.ico` file named `icono.ico`. You can use a free online converter for this (e.g., search for "PNG to ICO converter").
2.  Once you have the `icono.ico` file, place it in the same `Functions/luna/Assets/` directory.

## Step 2: Build the Executable

The `build.py` script automates the process of creating the `Selene.exe` executable.

1.  Open a Command Prompt or PowerShell.
2.  Navigate to the root directory of the Selene project.
3.  Run the build script using the following command:
    ```
    python release/build.py
    ```
4.  If the build is successful, a `dist` directory will be created in the project root, containing `Selene.exe`.

## Step 3: Create the Installer

The `installer.nsi` script uses NSIS to package `Selene.exe` into a user-friendly installer.

1.  Right-click on the `release/installer.nsi` file.
2.  Select **"Compile NSIS Script"** from the context menu. This option will be available if you installed NSIS correctly.
3.  NSIS will compile the script, and if successful, it will create `Selene_Installer.exe` in the `release` directory.

## Step 4: Run the Installer

You can now run `Selene_Installer.exe` to install the Selene application on your system. The installer will create a shortcut in the Start Menu for easy access.

---
If you encounter any issues, please ensure that all prerequisites are installed correctly and that you are running the commands from the project's root directory.