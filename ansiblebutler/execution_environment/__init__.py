from ._initialize import init_dir

def do_ee_action(args: dict, config: dict):
  context_dir = args.get('<dir>') or './'
  if args.get('init'):
    init_dir(context_dir, config['init'])
  else:
    raise Exception("Invalid option for ee (execution environment)")