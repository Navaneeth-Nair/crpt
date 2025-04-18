@echo off
set PROJECT_DIR=c:\Development\github-clone-crypt
C:\Python313\python.exe -c "import sys; sys.path.insert(0, r'%PROJECT_DIR%'); from crpt.crpt import main; main()"