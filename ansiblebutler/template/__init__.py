from ..common.auth import get_controller_auth
from ._clone import do_clone


def do_template_action(args: dict, config: dict):
  auth = get_controller_auth(config)
  if args.get('clone'):
    do_clone(args, config['clone'], auth)
