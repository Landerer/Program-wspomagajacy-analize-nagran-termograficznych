from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
options = {
    "build_exe": {
        "packages": ["pyqtgraph.debug", "pyqtgraph.reload"],
        "includes": "atexit",
    }
}

import sys

base = "Win32GUI" if sys.platform == "win32" else None
# base = "Console"

executables = [Executable("application.py", base=base, target_name="ObjawRaynauda")]

setup(
    name="ObjawRaynauda",
    version="1.0",
    author="Klaudia Krasicka",
    author_email="klaudia.krasicka97@gmail.com",
    description="Pomoc w diagnozowaniu objawu Raynauda",
    url="https://github.com/Landerer/objawRaynauda",
    options=options,
    executables=executables,
)
