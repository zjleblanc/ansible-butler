from ansiblelint.runner import Runner
from ansiblelint.rules import RulesCollection
from ansiblelint.file_utils import Lintable
from ansiblelint.utils import Task
from ansible.plugins.loader import module_loader
from ..common import default_json_serializer
import json

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

def _process_tasks(tasks_file: Lintable, collections: dict):
  for raw_task in tasks_file.data:
    lint_task = Task(raw_task)
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
  children = filter(lambda c: c.kind == 'tasks', runner.find_children(playbook))

  collections = _process_playbook(playbook)
  for child in children:
    collections = _process_tasks(child, collections)

  # print(json.dumps(collections, default=default_json_serializer, indent=2))
  print_report(playbook.name, collections)