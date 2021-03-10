@echo off

rem setLocal EnableDelayedExpansion

SET HOMEBIN=%HOMEDRIVE%%HOMEPATH%\bin
SET PYENV_PY=pyenv.py


if "%1"=="" (
  echo ===================================================
  echo Python Virtual Environment Helper
  echo ===================================================
  echo --list Lists all environments
  echo --long_list Lists env
  echo --act [env name] for activating an environment
  echo --deact for deactivating an environment
  GOTO :END
  )

set COMMAND=%1
set VENV=%2


SET TEMP_BAT=%HOMEBIN%\__tmp__.bat

echo "dummy" > %TEMP_BAT%
del /q  %TEMP_BAT%


if "%COMMAND%"=="--act" (
   python %PYENV_PY% --show_activate_path %VENV% 1>%TEMP_BAT% 2>%HOMEBIN%\err.txt
   CALL %TEMP_BAT%
)

if "%COMMAND%"=="--deact" (
   %VIRTUAL_ENV%\Scripts\deactivate.bat
)

if "%COMMAND%"=="--select" (
   python %PYENV_PY% --select %TEMP_BAT% 2>%HOMEBIN%\err.txt
   CALL %TEMP_BAT%
)


if "%COMMAND%"=="--list" (
  python %PYENV_PY% --list
)

if "%COMMAND%"=="--long_list" (
  python %PYENV_PY% --long_list
)

if "%COMMAND%"=="create" (
  python -m venv V:\%VENV%
)


:END
