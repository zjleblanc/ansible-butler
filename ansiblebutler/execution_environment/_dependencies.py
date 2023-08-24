import json
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

def desc_deps(definition_path: str, config: dict):
  resolver = DependencyResolver()
  definition = load_yml(definition_path)
  resolver.resolve(definition['collections'])
  print("Dependencies Identified")
  print("-----------------------")
  print(json.dumps(resolver.dependencies, indent=2))

  py_deps = resolver.dependencies.get('python',[])
  if len(py_deps):
    reqs = map(lambda line: line.lstrip().split(' ')[0], py_deps)
    print("\nBeginning pip *dry-run*\t(Nothing will be installed)")
    print("-----------------------")
    pip_dry_run(reqs)