import os
from ..common import parse_yml, parse_comment_lines, parse_comment_line_endings, get_template

TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/templates'

def mk_readme(role: str):
  role_name = os.path.basename(role)
  template_vars = {
    "role_name": role_name,
    "meta": {
      "galaxy_info": {}
    },
    "defaults": {}
  }
  template_vars.update(get_yaml_dict(role + '/meta/main.yml', 'meta'))
  template_vars.update(get_defaults(role + '/defaults/main.yml'))
  template_vars.update(get_required_vars(role + '/defaults/main.yml', 'required_vars'))
  template_vars.update(get_yaml_dict(role + '/vars/main.yml', 'vars'))
  template_vars.update(get_yaml_dict(role + '/handlers/main.yml', 'handlers'))
  
  template = get_template('README.md.j2', TEMPLATE_DIR)
  template.stream(template_vars).dump(role + '/README-butler.md')

def get_defaults(yml):
  defaults = get_yaml_dict(yml)
  comments = parse_comment_line_endings(yml)
  return { "defaults": defaults, "default_comments": comments }

def get_yaml_dict(yml, key=None) -> dict:
  if os.path.isfile(yml):
    parsed = parse_yml(yml) or {}
  else:
    return {}

  if key:
    return { key: parsed }
  return parsed or {}

def get_required_vars(yml, key=None) -> dict:
  if os.path.isfile(yml):
    parsed = parse_comment_lines(yml) or {}
  else:
    return {}

  if key:
    return { key: parsed }
  return parsed or {}