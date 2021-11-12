@echo off

rem setLocal EnableDelayedExpansion

SET HOMEBIN=%HOMEDRIVE%%HOMEPATH%\bin
SET PYENV_PY=%HOMEBIN%\pyenv.py
rem SET PYENV_PY=pyenv.py

if "%1"=="" (
  echo ===================================================
  echo Python Virtual Environment Helper
  echo ===================================================
  echo --version Prints Version
  echo --list Lists all environments
  echo --long_list Lists env
  echo --create [env name] creates an environment
  echo --delete [env name] deletes an environment
  echo --act [env name] for activating an environment
  echo --select Create list to select an environment for activation
  echo --deact for deactivating an environment
  echo --show_config shows the configuration data
  GOTO :END
  )

set COMMAND=%1
set VENV=%2


SET TEMP_BAT=%HOMEBIN%\__tmp__.bat

echo "dummy" > %TEMP_BAT%
del /q  %TEMP_BAT%



if "%COMMAND%"=="--version" (
   python %PYENV_PY% --version
)

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

if "%COMMAND%"=="--create" (
  python %PYENV_PY% --create %VENV%
)

if "%COMMAND%"=="--delete" (
  python %PYENV_PY% --delete %VENV%
)

if "%COMMAND%"=="--long_list" (
  python %PYENV_PY% --long_list
)


if "%COMMAND%"=="--show_config" (
   python %PYENV_PY% --show_config
)

:END
