import subprocess
import os
import sys

def main():
    """
    Compiles the Selene project into a single executable for Windows.
    This script should be run from the project's root directory.
    e.g., python release/build.py
    """
    # Ensure the script is run from the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if os.getcwd() != project_root:
        print(f"Changing current directory to project root: {project_root}")
        os.chdir(project_root)

    icon_path_png = os.path.join('Functions', 'luna', 'Assets', 'icono.png')
    icon_path_ico = os.path.join('Functions', 'luna', 'Assets', 'icono.ico')

    # PyInstaller on Windows requires an .ico file.
    # We check for it and provide instructions if it's missing.
    if not os.path.exists(icon_path_ico):
        print(f"Error: Icon file '{icon_path_ico}' not found.")
        print(f"Please convert '{icon_path_png}' to a .ico file and place it in the same directory.")
        print("There are free online tools available to convert PNG to ICO.")
        sys.exit(1)

    # Command to build the executable
    command = [
        'pyinstaller',
        '--onefile',
        '--name', 'Selene',
        '--icon', icon_path_ico,
        'selene.py'
    ]

    print(f"Running command: {' '.join(command)}")

    try:
        # Run the command from the project root
        subprocess.run(command, check=True, cwd=project_root)
        print("\nBuild successful! The executable can be found in the 'dist' directory.")
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with error: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("\nError: 'pyinstaller' command not found.")
        print("Please make sure PyInstaller is installed (`pip install pyinstaller`).")
        sys.exit(1)

if __name__ == '__main__':
    main()