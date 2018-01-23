from cx_Freeze import setup,Executable

executable_ = [Executable("main.py")]

setup(
	name="Geimu",
	options={"build.exe":{"packages":["pygame"]}},
	executables = executable_

)