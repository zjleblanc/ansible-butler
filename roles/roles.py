import os
import glob

from ._clean import clean_role
from ._list import list_role
from ._mkreadme import mk_readme

def do_roles_action(args: dict):
  roles_path = args.get('--roles-path')
  dir_glob = args.get('<name>') or "*"
  for role in glob.glob(roles_path + "/" + dir_glob):
    if os.path.isdir(role):
      if args.get('list'):
        list_role(role)
      elif args.get('clean'):
        clean_role(role)
      elif args.get('mk-readme'):
        mk_readme(role)
      else:
        list_role(role)
