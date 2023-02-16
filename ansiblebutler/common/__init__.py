import os
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template

TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/templates'

CONFIG_FILE_NAME = '.ansible-butler.yml'
CONFIG_LOCATIONS = [
  ## order matters
  '/etc/ansible-butler', ## least precedence
  str(Path.home()),
  os.getcwd() ## highest precedence
  
]

def load_yml(path):
  if os.path.isfile(path):
    with open(path, 'r') as yml:
      return yaml.safe_load(yml)
  return {}

def process_config(custom):
  defaults = os.path.join(os.path.dirname(__file__), CONFIG_FILE_NAME)
  config = load_yml(defaults)

  for loc in CONFIG_LOCATIONS:
    path = loc + '/' + CONFIG_FILE_NAME
    config.update(load_yml(path))

  if custom:
    config.update(load_yml(custom))

  return config

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