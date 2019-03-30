# !/usr/bin/env python
#coding: utf-8

import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None

if sys.platform == "win32":
    base = "Win32GUI"

if sys.platform == 'win64':
    base = "Win64GUI"

"""options = {
    'build_exe': {
        'includes': 'atexit'
    }
}
"""
"""build_exe_options = {"packages": ["os"],
                     'includes': 'atexit'}
"""
build_exe_options = {"packages": ["os",
                                  "numpy"],
                     "includes":["numpy"],
                     "include_files":["VSOP87D.ear",
                                     "cursor",
                                     "icons",
                                      "data"]
}

setup(
    name = "digisun",
    version = "1.1",
    description = "GUI to extract data from sunspot drawing",
    options = {"build_exe": build_exe_options}, #options,
    executables = [Executable("digisun.py", base=base, icon="digisun.ico")]
)
