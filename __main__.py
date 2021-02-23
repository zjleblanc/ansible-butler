"""
Usage: 
  ansible-butler.py roles list [--roles-path=PATH] [<glob>]
  ansible-butler.py roles clean [<name>]

Options:
  -h --help                               Show this screen
  --roles-path=PATH   Path to roles directory [default: ./roles]
"""
from docopt import docopt
from roles import list_roles

def main(args: dict):
  if args.get('roles'):
    list_roles(args)
  else:
    print(args)

if __name__ == '__main__':
    main(docopt(__doc__))