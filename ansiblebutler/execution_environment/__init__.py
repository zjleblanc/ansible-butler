from ._initialize import init_def
from ._inspect import inspect_ee
from ._dependencies import desc_deps

def do_ee_action(args: dict, config: dict):
  context_dir = args.get('<dir>') or './'
  if args.get('init'):
    init_def(context_dir, config['init'])
  elif args.get('inspect'):
    inspect_ee(args.get('<image>'), config['inspect'])
  elif args.get('dependencies') or args.get('deps'):
    desc_deps(args.get('<name>'), config['dependencies'])
  else:
    raise Exception("Invalid option for ee (execution environment)")