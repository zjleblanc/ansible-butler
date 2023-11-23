import os
import glob

from ._clean import clean_role
from ._list import list_role
from ._mkreadme import mk_readme
from ._deps import get_role_dependencies

def do_role_action(args: dict, config: dict):
  roles_path = args.get('--roles-path')
  roles = glob.glob(roles_path + "/*", recursive=args.get('--recursive', False))

  if args.get('deps', args.get('dependencies')):
    master_node = args.get('<master>') or config.get('dependencies').get('master_node', 'undefined')
    get_role_dependencies(roles, args.get('<master>'), config.get('dependencies'))
    return

  for role in roles:
    if os.path.isdir(role):
      if args.get('list'):
        list_role(role)
      elif args.get('clean'):
        clean_role(role)
      elif args.get('mk-readme'):
        mk_readme(role)
      else:
        list_role(role)
