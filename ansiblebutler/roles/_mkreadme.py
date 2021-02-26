import os
from ._common import parse_yml, get_template

def mk_readme(role: str):
  role_name = os.path.basename(role)
  template_vars = {
    "role_name": role_name,
    "meta": {},
    "defaults": {}
  }
  template_vars.update(get_yaml_dict(role + '/meta/main.yml', 'meta'))
  template_vars.update(get_yaml_dict(role + '/defaults/main.yml', 'defaults'))
  template_vars.update(get_yaml_dict(role + '/vars/main.yml', 'vars'))
  template_vars.update(get_yaml_dict(role + '/handlers/main.yml', 'handlers'))
  
  template = get_template('README.md.j2')
  template.stream(template_vars).dump(role + '/README-butler.md')

def get_yaml_dict(yml, key=None) -> dict:
  parsed = {}
  if os.path.isfile(yml):
    parsed = parse_yml(yml)

  if key:
    return { key: parsed }
  return parsed