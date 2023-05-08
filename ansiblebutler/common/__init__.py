import os
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template
from mergedeep import merge, Strategy

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
    merge(config, load_yml(path), strategy=Strategy.TYPESAFE_REPLACE)

  if custom:
    merge(config, load_yml(custom), strategy=Strategy.TYPESAFE_REPLACE)

  return config

def parse_yml(yml: str):
  yml_dict = None
  with open(yml, 'r') as stream:
    try:
      yml_dict = yaml.safe_load(stream)
    except yaml.YAMLError as ex:
      print(ex)
  return yml_dict

def parse_comment_lines(yml):
  comments = []
  with open(yml, 'r') as stream:
    for line in stream.readlines():
      if line.startswith("#") and len(line.split("#")) > 1:
        comment = {}
        parts = line.strip("#").split("#")
        comment['name'] = parts[0].strip()
        if ":" in comment['name']:
          comment['value'] = comment['name'].split(":")[1].strip()
          comment['name'] = comment['name'].split(":")[0].strip()
        if len(parts) > 1:
          comment['desc'] = parts[-1].strip()
        comments.append(comment)
  return comments

def parse_comment_line_endings(yml):
  var_comments = {}
  with open(yml, 'r') as stream:
    for line in stream.readlines():
      if not line.strip().startswith("#") and "#" in line:
        parts = line.strip().split("#")
        var_name = parts[0].split(":")[0].lstrip()
        var_comment = parts[-1].lstrip()
        var_comments[var_name] = var_comment
  return var_comments

def get_template(name: str, templates_dir=TEMPLATE_DIR) -> Template:
  file_loader = FileSystemLoader(templates_dir)
  env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)
  return env.get_template(name)