from ._initialize import init_dir
from ._clean import clean_dir

def do_dir_action(args: dict):
  context_dir = args.get('<dir>') or './'
  if args.get('init'):
    init_dir(context_dir)
  elif args.get('clean'):
    clean_dir(context_dir, args.get('--skip-roles'))
  else:
    raise Exception("Invalid option for directory")