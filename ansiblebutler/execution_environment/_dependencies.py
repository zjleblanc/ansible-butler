import json
import os
from ..common import load_yml
from ..common.dependencies import DependencyResolver, parse_python_reqs

def pip_dry_run(requirements: list[str]):
  from pip._internal.cli.main_parser import parse_command
  from pip._internal.commands import create_command

  cli_args = ['install','--dry-run']
  cli_args.extend(requirements)
  cmd_name, cmd_args = parse_command(cli_args)
  command = create_command(cmd_name, isolated=False)
  options, args = command.parse_args(cli_args)
  try:
    command.main(args)
    command.run(options, args)
  except AssertionError:
    pass # Ignore context related error using CLI from code

def get_python_reqs(definition, path) -> list[str]:
  if not definition.get('dependencies', {}).get('python', None):
    return []
  python = definition['dependencies']['python']
  
  if isinstance(python, str):
    return parse_python_reqs(os.path.dirname(path) + '/' + python)
  if isinstance(python, list):
    return python
  return []

def get_collections(definition, path) -> list[str]:
  # process requirements.yml
  if 'collections' in definition:
    return definition['collections']
  # process execution-environment.yml
  if 'dependencies' in definition:
    galaxy = definition['dependencies'].get('galaxy', None)
    if not galaxy:
      return []
    if isinstance(galaxy, str):
      reqs_file = os.path.dirname(path) + '/' + galaxy
      reqs_from_file = load_yml(reqs_file)
      return get_collections(reqs_from_file, reqs_file)
    if isinstance(galaxy, dict):
      return definition['dependencies']['galaxy'].get('collections', [])
  # unexpected file type
  print(f"[WARNING]Found unexpected contents in {path} - please confirm this is a requirements file or execution environment definition")
  return []

def desc_deps(definition_path: str, config: dict):
  resolver = DependencyResolver()
  definition = load_yml(definition_path)
  collections = get_collections(definition, definition_path)
  resolver.resolve(collections)
  print("Dependencies Identified")
  print("-----------------------")
  print(json.dumps(resolver.dependencies, indent=2))

  python_deps = get_python_reqs(definition, definition_path)
  python_deps.extend(resolver.dependencies.get('python',[]))
  if len(python_deps):
    reqs = map(lambda line: line.lstrip().split(' ')[0], python_deps)
    print("\nBeginning pip *dry-run*\t(Nothing will be installed)")
    print("-----------------------")
    pip_dry_run(reqs)