#!/usr/bin/env bash

if [ -z $1 ]; then
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
  echo --show_config shows the configuration data
  echo ""
  echo To deactivate an environment, call \"deactivate\" in the bash shell
  echo ""
  exit 0
fi

PYENV_PY=pyenv.py
COMMAND=$1
VENV=$2


if [ "$COMMAND" = "--version" ]; then
  python3 $PYENV_PY --version
  exit 0
fi

if [ "$COMMAND" = "--list" ]; then
  python3 $PYENV_PY --list
  exit 0
fi

if [ "$COMMAND" = "--long_list" ]; then
  python3 $PYENV_PY --long_list
  exit 0
fi

if [ "$COMMAND" = "--create" ]; then
  python3 $PYENV_PY --create $VENV
  exit 0
fi

if [ "$COMMAND" = "--delete" ]; then
  python3 $PYENV_PY --delete $VENV
  exit 0
fi

if [ "$COMMAND" = "--act" ]; then
  python3 $PYENV_PY --activate_on_linux $VENV
  bash
  exit 0
fi

if [ "$COMMAND" = "--select" ]; then
  python3 $PYENV_PY --select_on_linux
  bash
  exit 0
fi

if [ "$COMMAND" = "--show_config" ]; then
  python3 $PYENV_PY --show_config
  exit 0
fi
