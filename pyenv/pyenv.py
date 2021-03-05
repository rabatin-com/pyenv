#!/usr/bin/env python3

# ---------------------------------------------
# Copyright Arthur Rabatin. See www.rabatin.com
# ---------------------------------------------

import sys
from pathlib import Path

VENV_PATH = Path('V:/')

def list_env(venv_path:Path):
  return [x.name for x in venv_path.iterdir()]

if __name__ == '__main__':

  if len(sys.argv) >= 2:
    if sys.argv[1] == 'list':
      for d in list_env(VENV_PATH):
        print(d)




