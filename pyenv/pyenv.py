#!/usr/bin/env python3

# ---------------------------------------------
# Copyright Arthur Rabatin. See www.rabatin.com
# ---------------------------------------------

import collections
import sys
from pathlib import Path
import json
import yaml
import argparse
import os
import subprocess

CONFIGFILE = Path('pyenv_config.yaml')


class VenvEnv:

  def __init__(self):
    self.vens = {}

  def add_from_path(self, venvpath_root:Path):
    loaded_paths = [x for x in Path(venvpath_root).iterdir()]
    for p in loaded_paths:
      if Path(p/'pyvenv.cfg').is_file():
        with open(Path(p/'pyvenv.cfg'), 'r') as fp:
          cfg = fp.readlines()
        if p.name in self.vens:
          print(f'Ingnoring {p.name}: Error - Environment found in  {p} but already found in {self.vens[p.name]["path"]}', file=sys.stderr)
        else:
          self.vens[p.name] = {}
          self.vens[p.name]['path'] = p
          for line in cfg:
            self.vens[p.name][line.split('=')[0].strip()] = line.split('=')[1].strip()

if __name__ == '__main__':


  configfilelocations = [Path('.'), Path('~/.venv'), Path('~/.pyenv'), Path('~'), Path('~/bin')]
  configfilelocations = list(map(lambda x:x.expanduser(), configfilelocations))

  configfile = None

  for loc in configfilelocations:
    if Path(loc/CONFIGFILE).is_file():
      configfile = Path(loc/CONFIGFILE)
      break

  with open(configfile, 'r') as fp:
    app_config = yaml.load(fp, Loader=yaml.FullLoader)
    # print(app_config)
  app_config['venv_paths'] = list(set(map(lambda x: str(Path(x).expanduser()), app_config['venv_paths']+[app_config['default_venv_path']])))

  venv = VenvEnv()
  for p in app_config['venv_paths']:
    venv.add_from_path(p)

  parser = argparse.ArgumentParser(prog='PYENV Helper',
                                   usage='Print -h for help',
                                   formatter_class=argparse.RawTextHelpFormatter
                                   )

  parser.add_argument('--list', help='Lists all environments', action='store_true')

  parser.add_argument('--long_list', help='Lists all environments', action='store_true')

  parser.add_argument('--select', nargs=1, help='Select from environments', action='store')

  parser.add_argument('--create', nargs=1, help='Create an environment in the default location',
                      action='store')

  parser.add_argument('--show_config', help='Shows Config', action='store_true')

  parser.add_argument('--show_activate_path', nargs=1, help='Prints Activate Path', action='store')


  app_args = parser.parse_args()

  if app_args.show_config:
    print(f'Looking for {CONFIGFILE} in {configfilelocations}')
    print(f'Found {configfile.absolute()}')
    print(json.dumps(app_config, indent=2))

  if app_args.show_activate_path:
    envname = app_args.show_activate_path[0]
    activate_path = Path(Path(venv.vens[envname]['path']) / 'Scripts' / 'activate.bat')
    print(activate_path)

  if app_args.list:
    for env in venv.vens:
      print(env)

  if app_args.long_list:
    for k, v in venv.vens.items():
      print(k, ' Version:', v['version'], ' Location:', v['path'])

  if app_args.create:
    venv_name = app_args.create[0]
    if venv_name in venv.vens:
      print(f'Virtual Environment {venv_name} already exists',file=sys.stderr)
      exit(1)
    venv_full_path = Path(Path(app_config['default_venv_path']) / venv_name)
    cmd = f'python -m venv {str(venv_full_path)}'
    completed = subprocess.run(cmd)
    if completed.returncode != 0:
      print(f'Error in executing command {cmd}', file=sys.stderr)
      print(f'{completed.stderr}', file=sys.stderr)


  if app_args.select:
    envlist = []
    for envname, data in venv.vens.items():
      envlist.append(envname)
    for e in envlist:
      print (f'{envlist.index(e)}: {e}')
    selection = input('Enter your selection: ')
    activate_path = Path(Path(venv.vens[envlist[int(selection)]]['path']) / 'Scripts' / 'activate.bat')
    with open(app_args.select[0], 'w') as fp:
      print(activate_path, file=fp)





  






