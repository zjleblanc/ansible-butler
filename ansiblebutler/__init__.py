"""
Usage:
  ansible-butler directory init [<dir>] [--config=PATH]
  ansible-butler directory clean [<dir>] [--skip-roles]
  ansible-butler ee init [<dir>] [--config=PATH]
  ansible-butler ee inspect [<image>] [--config=PATH]
  ansible-butler ee [dependencies|deps] [--config=PATH] [<name>]
  ansible-butler role list [--roles-path=PATH] [<name> --recursive]
  ansible-butler role [dependencies|deps] [--roles-path=PATH] [<master>]
  ansible-butler role clean [--roles-path=PATH] [<name> --recursive]
  ansible-butler role mk-readme [--roles-path=PATH] [<name> --recursive]
  ansible-butler playbook update [--context=CONTEXT] [--config=PATH] [<name>] [--recursive] [--force]
  ansible-butler playbook [list-collections|lc] [--context=CONTEXT] [--config=PATH] [<name>] [--recursive] [--force]

Arguments:
  name    name of target (accepts glob patterns)
  image   name of image
  master  name of master node in graph
  dir     path to directory [default: ./]

Options:
  -h --help           Show this screen
  -r --recursive      Apply glob recursively [default: False]
  -f --force          Make file changes in place
  --config=PATH       Path to config file
  --roles-path=PATH   Path to roles directory [default: ./roles]
  --context=CONTEXT   Path to context directory [default: ./]
  --skip-roles        Flag to skip cleaning roles
"""
from docopt import docopt
from ansiblebutler import role
from ansiblebutler import directory
from ansiblebutler import execution_environment
from ansiblebutler import playbook
from ansiblebutler.common import process_config

def main():
  args = docopt(__doc__)
  config = process_config(args.get('--config'))

  if args.get('role'):
    role.do_role_action(args, config.get('role'))
  elif args.get('directory'):
    directory.do_dir_action(args, config.get('directory'))
  elif args.get('ee'):
    execution_environment.do_ee_action(args, config.get('execution_environment'))
  elif args.get('playbook'):
    playbook.do_playbook_action(args, config.get('playbook'))
  else:
    print(args)

if __name__ == '__main__':
  main()
