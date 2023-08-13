from ..common import PLUGIN_MAP_PATH, load_yml
from ansiblelint.utils import Task
from pathlib import Path

PLUGIN_MAP = load_yml(PLUGIN_MAP_PATH)

def get_ansible_type(parsed: dict) -> str:
    if isinstance(parsed, list) and len(parsed) > 0:
        if "hosts" in parsed[0]:
            return "playbook"
        else:
            return "tasks"
    return "undet"

def get_module_names(tasks: list) -> list:
    names = set()
    for t in tasks:
        task = Task(t)
        names.add(task["action"]["__ansible_module_original__"])
    return names

def update_module_names(content, module_names, module_map):
    for name in module_names:
        # preceding spaces / ending colon ensure matching text is a full yaml key
        content = content.replace(f'  {name}:', f'  {module_map[name]["redirect"]}:')
    return content

def update_playbook(ansible_path: str, **kwargs):
    parsed = load_yml(ansible_path)
    ansible_type = get_ansible_type(parsed)
    module_names = set()
    
    if ansible_type == "playbook":
        for play in parsed:
            tasks = play.get('tasks', [])
            module_names = module_names.union(get_module_names(tasks))
    elif ansible_type == "tasks":
        module_names = get_module_names(parsed)
    else:
        raise Exception(f"Unable to parse ansible file: {ansible_path}")
    
    module_map = PLUGIN_MAP['modules']
    module_map.update(kwargs['config'].get('modules', {}))
    updated = update_module_names(Path(ansible_path).read_text(), module_names, module_map)
    
    if kwargs['in_place']:
        Path(ansible_path).write_text(updated)
    else:
        butler_path = ansible_path.replace(".yml", ".butler.yml")
        Path(butler_path).write_text(updated)