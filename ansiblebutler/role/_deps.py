import os
import json

import ansible.constants as C
from ansiblelint.runner import Runner
from ansiblelint.rules import RulesCollection
from ansiblelint.file_utils import Lintable
from ansiblelint.utils import Task
from ..common import load_yml, dump_json, template_html

TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/templates'

def _normalize_dependency(dep) -> str:
  if 'role' in dep:
    return dep.get('role')
  elif 'src' in dep:
    return dep.get('src').split('/')[-1]
  else:
    raise ValueError

def _process_tasks(role: str):
  if not os.path.exists(role + '/tasks/main.yml'):
    return [], 0
  
  rules = RulesCollection()
  runner = Runner(role, rules=rules)
  tasks_all = Lintable(role + '/tasks/main.yml')
  if not tasks_all.data:
    return [], 0

  task_data = tasks_all.data
  for included in list(filter(lambda c: c.kind == 'tasks', runner.find_children(tasks_all))) or []:
    task_data.extend(included.data)

  dependencies = []
  for raw_task in task_data:
    lint_task = Task(raw_task)
    try:
      if lint_task.get('action') and lint_task.action.endswith("include_role") and lint_task.args.get('name'):
        dependencies.append(lint_task.args.get('name'))
    except Exception as ex:
      print(f"[Processing role {role}] Failed to parse {raw_task['__file__']} with Exception: {ex}")
  return dependencies, len(task_data)

def _process_play(play):
  roles = map(lambda rm: rm if isinstance(rm, str) else rm.get('role', 'unknown'), play.get('roles', []))
  dependencies = list(roles)
  for task in map(lambda t: Task(t), play.get('tasks', [])):
    if task.get('action') and task.action.endswith("include_role") and task.args.get('name'):
      dependencies.append(task.args.get('name'))
  return filter(lambda r: not r.startswith('../..'), dependencies)

def _process_role_tests(role: str):
  dependencies = []
  for root, dirs, files in os.walk(role + '/tests'):
    playbooks = filter(lambda f: not f.startswith('requirements') and f.endswith('.yml'), files)
    C.set_constant('DUPLICATE_YAML_DICT_KEY', 'ignore')
    C.set_constant('DEPRECATION_WARNINGS', False)
    lintables = map(lambda pb: Lintable(f"{root}/{pb}"), playbooks)
    for pb in filter(lambda l: l.kind == 'playbook', lintables):
      try:
        for play in pb.data:
          dependencies.extend(_process_play(play))
      except Exception as ex:
        print(f"[Processing role {role}] Failed to parse test playbook {pb.name} with Exception: {ex}")
  return dependencies

def _process_role(role: str, include_tests: False) -> dict:
  role_name = os.path.basename(role)
  # meta
  meta = load_yml(role + '/meta/main.yml') or {}
  dependencies = list(map(_normalize_dependency, meta.get('dependencies', [])))
  # tasks
  included, task_count = _process_tasks(role)
  dependencies.extend(included)
  # test playbooks
  if include_tests:
    dependencies.extend(_process_role_tests(role))
  # unique
  dependencies = set(dependencies)

  return { 
    "_name": role_name,
    "_deps": sorted(dependencies),
    "Tasks": task_count,
    "Min Ansible": meta.get('galaxy_info', {}).get('min_ansible_version', 'undefined') 
  }

def get_role_dependencies(roles: list[str], master: str, config: dict):
  dependencies = list(map(lambda role: _process_role(role, config.get('include_tests', False)), sorted(roles)))
  master_node = master or config.get('master_node', 'undefined')
  output_format = config.get('output_fmt')
  if output_format == 'json':
    output_dest = config.get('output_dest', 'graph.json')
    dump_json(dependencies, output_dest)
  else:
    output_dest = config.get('output_dest', 'graph.html')
    template_vars = config
    template_vars.update({"master_node": master_node, "dependencies": dependencies})
    template_html(template_vars, TEMPLATE_DIR, 'graph.html.j2', output_dest)