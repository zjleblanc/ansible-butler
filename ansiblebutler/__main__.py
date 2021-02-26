"""
Usage:
  ansible-butler.py role list [--roles-path=PATH] [<name>]
  ansible-butler.py role clean [--roles-path=PATH] [<name>]
  ansible-butler.py role mk-readme [--roles-path=PATH] [<name>]

Arguments:
  name    name of role (accepts glob patterns)

Options:
  -h --help                               Show this screen
  --roles-path=PATH   Path to roles directory [default: ./roles]
"""
from docopt import docopt
from ansiblebutler import main

if __name__ == '__main__':
  main()
