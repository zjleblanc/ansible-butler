import os
import glob
from ._update import update_playbook

def process_playbooks(fn, playbooks, config={}, in_place=False):
   for playbook in playbooks:
      if ".butler." not in playbook and not os.path.isdir(playbook):
        fn(playbook, config.get('update', {}), in_place)

def do_playbook_action(args: dict, config: dict):
  context_dir = args.get('--context')
  glob_filter = args.get('<name>') or "*.yml"
  playbooks = glob.glob(context_dir + "/" + glob_filter, recursive=args.get('--recursive', False))
  in_place = args.get('--force', False)
  if args.get('update'):
    process_playbooks(update_playbook, playbooks, config, in_place)
  else:
    raise Exception("Invalid option for ee (execution environment)")