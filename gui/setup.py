# A simple setup script to create an executable using PyQt5. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# PyQt5app.py is a very simple type of PyQt5 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

options = {"build_exe": {
    "includes": "atexit",
    "path": sys.path + ["csvtodb"]
}}

executables = [Executable("gui.py", base=base)]

setup(
    name="CsvToDB",
    version="0.1",
    description="GUI version to convert csv to db",
    options=options,
    executables=executables,
)
