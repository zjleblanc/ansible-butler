import os
import yaml
from jinja2 import Environment, FileSystemLoader, Template

TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/templates'

def parse_yml(yml: str):
  yml_dict = None
  with open(yml, 'r') as stream:
    try:
      yml_dict = yaml.safe_load(stream)
    except yaml.YAMLError as ex:
      print(ex)
  return yml_dict

def get_template(name: str, templates_dir=TEMPLATE_DIR) -> Template:
  file_loader = FileSystemLoader(templates_dir)
  env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)
  return env.get_template(name)