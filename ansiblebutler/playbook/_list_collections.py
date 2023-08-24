import os
from ansiblelint.runner import Runner
from ansiblelint.rules import RulesCollection
from ansiblelint.file_utils import Lintable
from ansiblelint.utils import Task, parse_yaml_from_file
from ansible.plugins.loader import module_loader
from ..common.dependencies import get_role_paths

def _get_task_collection(task: Task):
  module = module_loader.find_plugin_with_context(task.action)
  if not module.plugin_resolved_collection:
    print(f"WARNING: Collection not found for module '{module.original_name}'")
    return "unknown.unknown"
  return module.plugin_resolved_collection

def _process_playbook(playbook: Lintable):
  collections = {}
  for play in filter(lambda d: 'tasks' in d, playbook.data):
    for raw_task in play['tasks']:
      lint_task = Task(raw_task)
      collection_name = _get_task_collection(lint_task)

      if collection_name in collections:
        collections[collection_name]['count'] += 1
      else:
        collections[collection_name] = {
          "locations": set([playbook.name]),
          "count": 1
        }
  return collections

def _get_roles(play) -> list[str]:
  included_roles = []
  play_roles = play.get('roles', [])
  included_roles.extend(list(map(lambda role: role if not 'name' in role else role.get('name'), play_roles)))
  play_tasks = play.get('tasks', [])
  include_role_tasks = list(filter(lambda task: 'include_role' in task or 'ansible.builtin.include_role' in task, play_tasks))
  if len(include_role_tasks):
    role_names = list(map(lambda task: task.get('ansible.builtin.include_role', task.get('include_role')).get('name'), include_role_tasks))
    included_roles.extend(role_names)
  return included_roles

def _process_roles(playbook: Lintable, runner: Runner) -> list[Lintable]:
  included_tasks = []
  for play in parse_yaml_from_file(str(playbook.path)):
    role_names = _get_roles(play)
    if len(role_names):
      for role in role_names:
        role_search_paths = get_role_paths(role)
        for path in role_search_paths:
          role_path = path + "/" + role.split('.')[-1]
          if os.path.isdir(role_path):
            lintable = Lintable(role_path)
            if lintable.kind == 'role':
              included_tasks.extend(list(filter(lambda c: c.kind == 'tasks', runner.find_children(lintable))))
            break
  return included_tasks

def _process_tasks(tasks_file: Lintable, collections: dict):
  for raw_task in tasks_file.data:
    lint_task = Task(raw_task)
    if lint_task.action == "block/always/rescue":
      continue
    collection_name = _get_task_collection(lint_task)

    if collection_name in collections:
      collections[collection_name]['count'] += 1
      collections[collection_name]['locations'].add(tasks_file.name)
    else:
      collections[collection_name] = {
        "locations": set([tasks_file.name]),
        "count": 1
      }
  return collections

def print_report(path, collections):
  print(f"----- {path} -----\n")
  for coll in collections.keys():
    print(f"Collection: {coll}")
    print(f"Frequency: {collections[coll]['count']}")
    print(f"Locations:")
    for loc in collections[coll]['locations']:
      print(f"  - {loc}")
    print()

def list_collections(ansible_path: str):
  rules = RulesCollection()
  runner = Runner(ansible_path, rules=rules)
  playbook = Lintable(ansible_path)

  included_tasks = list(filter(lambda c: c.kind == 'tasks', runner.find_children(playbook))) or []
  included_tasks.extend(_process_roles(playbook, runner) or [])

  collections = _process_playbook(playbook)
  for child in included_tasks:
    collections = _process_tasks(child, collections)
  
  # print(json.dumps(collections, default=default_json_serializer, indent=2))
  print_report(playbook.name, collections)