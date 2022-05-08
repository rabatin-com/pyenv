#!/usr/bin/env python3

# ---------------------------------------------
# Copyright Arthur Rabatin. See www.rabatin.com
# ---------------------------------------------

import argparse
import json
import platform
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

import yaml

class OSPlatform:

  def __init__(self):
    self._is_linux = False
    self._is_windows = False
    if sys.platform.startswith('linux'):
      self._is_linux = True
    elif sys.platform.startswith('win'):
      self._is_windows = True
    else:
      raise Exception(f'Unknown Platform {sys.platform}')

  def is_linux(self):
    return self._is_linux

  def is_windows(self):
    return self._is_windows


CONFIGFILE = Path('hebi_config.yaml')

if OSPlatform().is_linux():
  PYTHON_EXEC = '/usr/bin/python3.8'
else:
  import warnings
  warnings.simplefilter('ignore', category=DeprecationWarning)
  from distutils import spawn
  PYTHON_EXEC = spawn.find_executable('python.exe')


VERSION = '1.0'


def activate_on_linux(environment_name: str):
  if not OSPlatform().is_linux():
    raise Exception('Platform is not Linux')
  activate_path = Path(Path(venv.vens[envname]['path']) / 'bin' / 'activate')
  if not activate_path.is_file():
    raise Exception(f'Is not a file: {activate_path}')
  dummy_hebi = Path('~/bin/__hebi_dummy__.tmp').expanduser()
  if not dummy_hebi.is_file():
    with open(dummy_hebi, 'w') as f:
      f.write('# Dummy Contents - Ignore\n')
  brc = BashRC(Path('~/bin/__hebi__.tmp').expanduser())
  if not brc.has_hebi_info:
    brc.write_hebi_info(activate_path)
  with open(Path('~/bin/__hebi__.tmp').expanduser(), 'w') as f:
    f.write(str(activate_path))


def read_deactive_command(activate_file: Path):
  if not activate_file.is_file():
    raise Exception(f'Does not exist {activate_file}')
  with open(activate_file, 'r') as f:
    rl = f.readlines()
  start_deactivate = -1
  end_deactivate = -1
  for idx, l in enumerate(rl):
    if l.startswith('deactivate ()'):
      start_deactivate = idx
    if start_deactivate >= 0:
      if l.startswith('}'):
        end_deactivate = idx
  return rl[start_deactivate:end_deactivate + 1]


class BashRC:
  HEBI_BEGIN = '# >>> HEBI Initialization >>>'
  HEBI_END = '# <<< HEBI Initialization <<<'

  def __init__(self, file_to_source: Path):
    self.source_file = Path(file_to_source).expanduser()
    self.bashrc = Path('~/.bashrc').expanduser()
    with open(self.bashrc, 'r') as f:
      rl = f.readlines()
    self.hebi_start = -1
    self.hebi_end = -1
    for idx, line in enumerate(rl):
      if line.startswith(BashRC.HEBI_BEGIN):
        self.hebi_start = idx
      if line.startswith(BashRC.HEBI_END):
        self.hebi_end = idx
    self.has_hebi_info = ((self.hebi_end - self.hebi_start) >= 2)
    # print(self.hebi_start, self.hebi_end, self.has_hebi_info)

  def write_hebi_info(self, activate_pathfile: Path):
    if self.has_hebi_info:
      raise Exception('Already has HEBI Info')
    with open(self.bashrc, 'a') as bashrc_f:
      bashrc_f.write('\n\n')
      bashrc_f.write('# *** DO NOT MODIFY THE HEBI INFORMATION MANUALLY ***\n')
      bashrc_f.write(f'{BashRC.HEBI_BEGIN}\n')
      bashrc_f.write(f'source `cat {self.source_file}`\n')
      bashrc_f.write(f'# Below the custom adoption of the deactivate command\n')
      deactive_text = read_deactive_command(activate_pathfile)
      if deactive_text[-1:][0] != '}\n':
        raise Exception('deactive_text unexpected' + str(deactive_text))
      deactive_text = deactive_text[:-1]
      dummy = Path('~/bin/__hebi_dummy__.tmp').expanduser()
      deactive_text.append('# Customization Start\n')
      deactive_text.append(f'    echo \"{dummy}\" > {self.source_file}\n')
      deactive_text.append('# Customization End\n')
      deactive_text.append('}\n')
      for code_line in deactive_text:
        bashrc_f.write(code_line)
      bashrc_f.write(f'{BashRC.HEBI_END}\n')
      bashrc_f.write('\n\n')




class VenvEnv:

  def __init__(self):
    self.vens = {}

  def add_from_path(self, venvpath_root: Path):
    venvpath_root = Path(venvpath_root)
    if not venvpath_root.is_dir():
      return
    loaded_paths = [x for x in Path(venvpath_root).iterdir()]
    for p in loaded_paths:
      # print(p)
      if Path(p / 'pyvenv.cfg').is_file():
        with open(Path(p / 'pyvenv.cfg'), 'r') as fp:
          cfg = fp.readlines()
        if p.name in self.vens:
          print(
            f'Ingnoring {p.name}: Error - Environment found in  {p} but already found in {self.vens[p.name]["path"]}',
            file=sys.stderr)
        else:
          self.vens[p.name] = {}
          self.vens[p.name]['path'] = p
          for line in cfg:
            self.vens[p.name][line.split('=')[0].strip()] = line.split('=')[1].strip()


if __name__ == '__main__':

  configfilelocations = [Path('.'), Path('~/.venv'), Path('~/.ar3_hebi'), Path('~'),
                         Path('~/bin')]
  configfilelocations = list(map(lambda x: str(x.expanduser()), configfilelocations))

  configfile = None

  for loc in configfilelocations:
    if Path(loc / CONFIGFILE).is_file():
      configfile = Path(loc / CONFIGFILE)
      break

  with open(configfile, 'r') as fp:
    app_config = yaml.load(fp, Loader=yaml.FullLoader)
  app_config['venv_paths'] = list(set(map(lambda x: str(Path(x).expanduser()),
                                          app_config['venv_paths'] + [
                                            app_config['default_venv_path']])))

  venv = VenvEnv()
  for p in app_config['venv_paths']:
    venv.add_from_path(p)

  parser = argparse.ArgumentParser(prog='PYENV Helper',
                                   usage='Print -h for help',
                                   formatter_class=argparse.RawTextHelpFormatter
                                   )

  parser.add_argument('--version', help='Displays Version Information',
                      action='store_true')

  parser.add_argument('--list', help='Lists all environments', action='store_true')

  parser.add_argument('--long_list', help='Lists all environments', action='store_true')

  parser.add_argument('--select', nargs=1, help='Select from environments',
                      action='store')

  parser.add_argument('--select_on_linux', help='Select from environments',
                      action='store_true')

  parser.add_argument('--create', nargs=1,
                      help='Create an environment in the default location',
                      action='store')

  parser.add_argument('--delete', nargs=1,
                      help='Deletes environment',
                      action='store')

  parser.add_argument('--show_config', help='Shows Config', action='store_true')

  parser.add_argument('--show_activate_path', nargs=1, help='Prints Activate Path',
                      action='store')

  parser.add_argument('--activate_on_linux', nargs=1, help='Activates VENV on Linux',
                      action='store')

  app_args = parser.parse_args()

  if app_args.version:
    print('HEBI VERSION', VERSION)
    print('Platform:', platform.version(), '\nPython Version:', platform.python_version())

  if app_args.show_config:
    print(f'Looking for {CONFIGFILE} in {configfilelocations}')
    print(f'Found {configfile.absolute()}')
    print(json.dumps(app_config, indent=2))

  if app_args.activate_on_linux:
    envname = app_args.activate_on_linux[0]
    activate_on_linux(envname)

  if app_args.show_activate_path:
    envname = app_args.show_activate_path[0]
    activate_path = 'Undefined - Not Set'
    if OSPlatform().is_windows():
      activate_path = Path(Path(venv.vens[envname]['path']) / 'Scripts' / 'activate.bat')
    if OSPlatform().is_linux():
      activate_path = Path(Path(venv.vens[envname]['path']) / 'bin' / 'activate')
    print(activate_path)

  if app_args.list:
    for env in venv.vens:
      print(env)

  if app_args.long_list:
    for modulename, venv_data in venv.vens.items():
      version = venv_data.get('version')
      if not version:
        version = venv_data.get('version_info', 'Undefined')
      location = venv_data['path']
      print(modulename, ' Version:', version, ' Location:', location)

  if app_args.create:
    venv_name = app_args.create[0]
    if venv_name in venv.vens:
      print(f'Virtual Environment {venv_name} already exists', file=sys.stderr)
      exit(1)
    venv_full_path = Path(Path(app_config['default_venv_path']) / venv_name)
    cmd = f'{PYTHON_EXEC} -m venv {str(venv_full_path.expanduser())}'
    completed = subprocess.run(
      [PYTHON_EXEC, '-m', 'venv', str(venv_full_path.expanduser())])
    if completed.returncode != 0:
      print(f'Error in executing command {cmd}', file=sys.stderr)
      print(f'{completed.stderr}', file=sys.stderr)

  if app_args.delete:
    venv_name = app_args.delete[0]
    if venv_name not in venv.vens:
      print(f'Virtual Environment {venv_name} does not exist', file=sys.stderr)
      exit(1)
    archive_path = Path(Path(app_config['default_venv_path']) / Path(
      'Archive') / f'{venv_name}-{uuid.uuid4()}').expanduser()
    archive_path.mkdir(parents=True, exist_ok=True)
    shutil.move(str(venv.vens[venv_name]['path']), str(archive_path))
    print(f'Removed {venv_name} into Archive')

  if app_args.select:
    envlist = []
    for envname, data in venv.vens.items():
      envlist.append(envname)
    for e in envlist:
      print(f'{envlist.index(e)}: {e}')
    selection = input('Enter your selection: ')
    activate_path = Path(
      Path(venv.vens[envlist[int(selection)]]['path']) / 'Scripts' / 'activate.bat')
    created_outputfile = app_args.select[0]
    print(created_outputfile, activate_path)
    with open(created_outputfile, 'w') as f:
      f.write(str(activate_path))

  if app_args.select_on_linux:
    envlist = []
    for envname, data in venv.vens.items():
      envlist.append(envname)
    for e in envlist:
      print(f'{envlist.index(e)}: {e}')
    selection = input('Enter your selection: ')
    envname = envlist[int(selection)]
    activate_on_linux(envname)
