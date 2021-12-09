import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "includes": ["tkinter", "mysql"]}

# GUI applications require a different base on Windows (the default is for
# a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Control",
    version="2.0",
    description="Controle de Finanças e Clientes",
    options={"build_exe": build_exe_options},
    executables=[Executable("Inicio.py", base=base, icon='Images/control.ico')]
)