import os
import ansible.constants as C
from ansible.galaxy.collection import find_existing_collections
from ansible.galaxy.collection.concrete_artifact_manager import ConcreteArtifactsManager
from ansible.cli.config import get_constants
from ansible.plugins.loader import init_plugin_loader
from ansiblelint.file_utils import Lintable
from ..external.introspect import process, sanitize_requirements

COLLECTIONS = None
ROLES_PATHS = C.config.get_config_value('DEFAULT_ROLES_PATH', variables=get_constants())
COLLECTION_PATHS = C.config.get_config_value('COLLECTIONS_PATHS', variables=get_constants())

def parse_python_reqs(requirements: str) -> list[str]:
  if isinstance(requirements, str):
    with open(requirements) as file:
      return [line for line in file]

def get_role_paths(role_name):
  paths = ROLES_PATHS
  paths.append('./roles')
  name_parts = role_name.split('.')
  if len(name_parts) == 3:
    collection_path = '/'.join(name_parts[:-1])
    paths.append('./ansible_collections/{collection_path}/roles')
    collection_role_paths = map(lambda p: f"{p}/ansible_collections/{collection_path}/roles", COLLECTION_PATHS)
    paths.extend((list(collection_role_paths)))
  return paths

class DependencyResolver():
  concrete_artifact_cm = ConcreteArtifactsManager(C.DEFAULT_LOCAL_TMP, validate_certs=False)
  missing_collections = []
  required_collections = []
  dependencies = None

  def __init__(self):
    init_plugin_loader()
    self.collection_paths = COLLECTION_PATHS
    self.available_collections = {}
    for coll in find_existing_collections(self.collection_paths, self.concrete_artifact_cm, dedupe=False):
      self.available_collections[coll.fqcn] = coll.src.decode('utf-8')

  def resolve(self, collections):
    self.get_coll_paths(collections)
    self.dependencies = process(self.required_collections)
    self.dependencies['python'] = sanitize_requirements(self.dependencies['python'])

  def get_coll_paths(self, collections) -> str:
    for coll in collections:
      name = self.__get_coll_name(coll)
      path = self.available_collections.get(name, None)
      if path:
        self.required_collections.append(path)
      else:
        self.missing_collections.append(name)

  def __get_coll_name(self, collection) -> str:
    if type(collection) == dict:
      return collection.get('name')
    return collection
  