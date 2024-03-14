import os
import yaml
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template
from mergedeep import merge, Strategy
from .butler_dumper import ButlerDumper

TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/templates'
PLUGIN_MAP_PATH = os.path.dirname(os.path.abspath(__file__)) + '/plugin_map.yml'

CONFIG_FILE_NAME = '.ansible-butler.yml'
CONFIG_LOCATIONS = [
  ## order matters
  '/etc/ansible-butler', ## least precedence
  str(Path.home()),
  os.getcwd() ## highest precedence
]

def process_config(custom):
  defaults = os.path.join(os.path.dirname(__file__), CONFIG_FILE_NAME)
  config = load_yml(defaults)

  for loc in CONFIG_LOCATIONS:
    path = loc + '/' + CONFIG_FILE_NAME
    merge(config, load_yml(path), strategy=Strategy.TYPESAFE_REPLACE)

  if custom:
    merge(config, load_yml(custom), strategy=Strategy.TYPESAFE_REPLACE)

  return config

def dump_yml(data, path: str):
  with open(path, 'w') as file:
    return yaml.safe_dump(data, file)
  
def dump_json(data, path: str, **kwargs):
  with open(path, 'w') as file:
    return json.dump(data, file, **kwargs)
  
def template_html(variables: dict, template_dir: str, template: str, path: str):
    template = get_template(template, template_dir)
    template.stream(variables).dump(path)

def load_yml(path: str):
  yaml_dict = {}
  if not os.path.isfile(path):
    return yaml_dict

  with open(path, 'r') as stream:
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


def __to_nice_yaml(data, level=0, indent=2):
    raw = yaml.dump(data, Dumper=ButlerDumper, indent=indent, sort_keys=False).rstrip()
    processed = map(lambda line: (" "*level*indent) + line, raw.split("\n"))
    return "\n".join(processed)

def get_template(name: str, templates_dir=TEMPLATE_DIR) -> Template:
  file_loader = FileSystemLoader(templates_dir)
  env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)
  env.filters['to_nice_yaml'] = __to_nice_yaml
  return env.get_template(name)

def default_json_serializer(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError