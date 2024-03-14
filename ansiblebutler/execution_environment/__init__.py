from ._initialize import init_dir
from ._dependencies import desc_deps

def do_ee_action(args: dict, config: dict):
  context_dir = args.get('<dir>') or './'
  if args.get('init'):
    init_dir(context_dir, config['init'])
  elif args.get('dependencies') or args.get('deps'):
    desc_deps(args.get('<name>'), config['dependencies'])
  else:
    raise Exception("Invalid option for ee (execution environment)")