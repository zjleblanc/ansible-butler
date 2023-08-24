import json
import os
from ..common import load_yml
from ..common.dependencies import DependencyResolver

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

def get_collections(definition_path) -> list[str]:
  definition = load_yml(definition_path)
  # process requirements.yml
  if 'collections' in definition:
    return definition['collections']
  # process ee v3
  if int(definition.get('version', -1)) == 3 and 'dependencies' in definition:
    galaxy = definition['dependencies'].get('galaxy', None)
    if not galaxy:
      return []
    if isinstance(galaxy, str):
      return get_collections(os.path.dirname(definition_path) + '/' + galaxy)
    if isinstance(galaxy, dict):
      return definition['dependencies']['galaxy'].get('collections', [])
  # process ee <= v2
  dependencies = definition.get('dependencies', {})
  if dependencies.get('galaxy', None):
    return get_collections(os.path.dirname(definition_path) + '/' + dependencies['galaxy'])
  # unexpected file type
  print(f"[WARNING]Found unexpected contents in {definition_path} - please confirm this is a requirements file or execution environment definition")
  return []

def desc_deps(definition_path: str, config: dict):
  resolver = DependencyResolver()
  collections = get_collections(definition_path)
  resolver.resolve(collections)
  print("Dependencies Identified")
  print("-----------------------")
  print(json.dumps(resolver.dependencies, indent=2))

  py_deps = resolver.dependencies.get('python',[])
  if len(py_deps):
    reqs = map(lambda line: line.lstrip().split(' ')[0], py_deps)
    print("\nBeginning pip *dry-run*\t(Nothing will be installed)")
    print("-----------------------")
    pip_dry_run(reqs)