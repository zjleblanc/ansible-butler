"""
Usage:
  ansible-butler.py roles list [--roles-path=PATH] [<name>]
  ansible-butler.py roles clean [--roles-path=PATH] [<name>]

Arguments:
  name    name of role (accepts glob patterns)

Options:
  -h --help                               Show this screen
  --roles-path=PATH   Path to roles directory [default: ./roles]
"""
from docopt import docopt
from roles import do_roles_action

def main(args: dict):
  if args.get('roles'):
    do_roles_action(args)
  else:
    print(args)

if __name__ == '__main__':
  main(docopt(__doc__))
