@echo off

FOR /R %%G IN (\test_files\*.txt) DO (
mpiexec -np 4 python mpiprim.py "%%G"
)
pause

