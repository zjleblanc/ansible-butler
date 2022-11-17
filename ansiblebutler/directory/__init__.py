from ._initialize import init_dir

def do_dir_action(args: dict):
  context_dir = args.get('--directory')
  init_dir(context_dir)