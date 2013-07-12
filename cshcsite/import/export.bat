@echo off
setlocal
for %%I in (*.mdb) do (
    if not exist "%%~nI//" mkdir "%%~nI"
    MDBtoCSV.exe "%%I" "%%~nI//"
)