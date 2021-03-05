@echo off

SET HOMEBIN=%HOMEDRIVE%%HOMEPATH%\bin
SET PYENV_PY=%HOMEBIN%\pyenv.py


if "%1"=="" (
  echo ===================================================
  echo Python Virtual Environment Helper
  echo ===================================================
  echo act [env name] for activating an environment
  echo create [env name] for activating an environment
  echo deact [env name] for deactivating an environment
  echo list for listing environments
  echo version for listing python versions per environment
  GOTO :END
  )

set COMMAND=%1
set VENV=%2


if "%COMMAND%"=="act" (
   echo Activate %VENV%
   V:\%VENV%\Scripts\activate.bat
)

if "%COMMAND%"=="list" (
  python %PYENV_PY% list
)

if "%COMMAND%"=="create" (
  python -m venv V:\%VENV%
)


if "%COMMAND%"=="version" (
    python %PYENV_PY% list > %HOMEBIN%\out.txt
    for /f "delims=" %%a in (%HOMEBIN%\out.txt) DO (
      V:\%%a\Scripts\python.exe --version > %HOMEBIN%\out2.txt
      SET /p xxVERSION=<%HOMEBIN%\out2.txt
      echo %%a: %xxVERSION%
    )
    del %HOMEBIN%\out.txt
    del %HOMEBIN%\out2.txt
)

if "%COMMAND%"=="deact" (
   V:\%VENV%\Scripts\deactivate.bat
)

:END
