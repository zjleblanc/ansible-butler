import os
from ..common import load_yml, parse_comment_lines, parse_comment_line_endings, get_template

TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/templates'

def mk_readme(role: str):
  role_name = os.path.basename(role)
  template_vars = {
    "role_name": role_name,
    "meta": {
      "galaxy_info": {}
    }
  }
  template_vars.update(get_yaml_dict(role + '/meta/main.yml', 'meta'))
  template_vars.update(get_yaml_dict(role + '/defaults/main.yml', 'defaults'))
  template_vars.update(get_yaml_dict(role + '/vars/main.yml', 'vars'))
  template_vars.update(get_yaml_dict(role + '/handlers/main.yml', 'handlers'))
  template_vars.update(get_required_vars(role + '/defaults/main.yml', 'required_vars'))
  
  template = get_template('README.md.j2', TEMPLATE_DIR)
  template.stream(template_vars).dump(role + '/README-butler.md')

def get_yaml_dict(yml, key) -> dict:
  if os.path.isfile(yml):
    parsed = load_yml(yml) or {}
    comments = parse_comment_line_endings(yml)
  else:
    parsed = {}
    comments = {}

  return { key: parsed, key + "_comments": comments }

def get_required_vars(yml, key) -> dict:
  if os.path.isfile(yml):
    return { key: parse_comment_lines(yml) or {} }
  else:
    return { key: {} }