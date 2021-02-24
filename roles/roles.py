import os
import glob
import yaml

def do_roles_action(args: dict):
  roles_path = args.get('--roles-path')
  dir_glob = args.get('<name>') or "*"
  for role in glob.glob(roles_path + "/" + dir_glob):
    if os.path.isdir(role):
      if args.get('list'):
        __list_role(role)
      elif args.get('clean'):
        __clean_role(role)
      else:
        __list_role(role)

def __list_role(role: str):
  print(os.path.basename(role))

def __clean_role(role: str):
  for yml in glob.glob(role + "/**/*.yml"):
    if not parse_yml(yml):
      os.remove(yml)

  for _dir in os.scandir(role):
    if os.path.isdir(_dir) and not os.listdir(_dir):
      os.rmdir(_dir)

def parse_yml(yml: str):
  yml_dict = None
  with open(yml, 'r') as stream:
    try:
      yml_dict = yaml.safe_load(stream)
    except yaml.YAMLError as ex:
      print(ex)
  return yml_dict
