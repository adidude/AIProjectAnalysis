import cx_Freeze, os
os.environ['TCL_LIBRARY'] = r'C:\Python27\tcl\tcl8.5'
os.environ['TK_LIBRARY'] = r'C:\Python27\tcl\tk8.5'
executables = [cx_Freeze.Executable("pygamePlot.py")]

cx_Freeze.setup(
    name="network",
    options={"build_exe": {"packages":["pygame", "snap"],
                           "include_files":["soc-sign-bitcoinotc.csv", "AI_Project.py", "config.txt"]}},
                            
    executables = executables

    )
