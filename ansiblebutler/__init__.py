"""
Usage:
  ansible-butler directory init [<dir>] [--config=PATH]
  ansible-butler directory clean [<dir>] [--skip-roles]
  ansible-butler ee init [<dir>] [--config=PATH]
  ansible-butler role list [--roles-path=PATH] [<name>]
  ansible-butler role clean [--roles-path=PATH] [<name>]
  ansible-butler role mk-readme [--roles-path=PATH] [<name>]

Arguments:
  name    name of role (accepts glob patterns)
  dir     path to directory [default: ./]

Options:
  -h --help           Show this screen
  --config=PATH       Path to config file
  --roles-path=PATH   Path to roles directory [default: ./roles]
  --skip-roles        Flag to skip cleaning roles
"""
from docopt import docopt
from ansiblebutler import roles
from ansiblebutler import directory
from ansiblebutler import execution_environment
from ansiblebutler.common import process_config

def main():
  args = docopt(__doc__)
  config = process_config(args.get('--config'))

  if args.get('role'):
    roles.do_roles_action(args, config.get('role'))
  elif args.get('directory'):
    directory.do_dir_action(args, config.get('directory'))
  elif args.get('ee'):
    execution_environment.do_ee_action(args, config.get('execution_environment'))
  else:
    print(args)

if __name__ == '__main__':
  main()
