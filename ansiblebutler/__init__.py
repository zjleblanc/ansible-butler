"""
Usage:
  ansible-butler directory init [<dir>]
  ansible-butler directory clean [<dir>] [--skip-roles]
  ansible-butler role list [--roles-path=PATH] [<name>]
  ansible-butler role clean [--roles-path=PATH] [<name>]
  ansible-butler role mk-readme [--roles-path=PATH] [<name>]

Arguments:
  name    name of role (accepts glob patterns)
  dir     path to directory [default: ./]

Options:
  -h --help                               Show this screen
  --roles-path=PATH   Path to roles directory [default: ./roles]
  --skip-roles        Flag to skip cleaning roles
"""
from docopt import docopt
from ansiblebutler import roles
from ansiblebutler import directory

def main():
  args = docopt(__doc__)
  if args.get('role'):
    roles.do_roles_action(args)
  elif args.get('directory'):
    directory.do_dir_action(args)
  else:
    print(args)

if __name__ == '__main__':
  main()
