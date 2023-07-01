import os
import glob
from ..common import load_yml

BASIC_TARGETS=[
    "filter_plugins",
    "library",
    "module_utils"
    "inventories"
]

def delete_empty_dirs(context: str):
    if not os.path.isdir(context):
        return

    for file in os.scandir(context):
        if os.path.isdir(file.path):
            delete_empty_dirs(file.path)

    if not os.listdir(context):
        os.rmdir(context)

def clean_role(role: str):
  for yml in glob.glob(role + "/**/*.yml"):
    if not load_yml(yml):
      os.remove(yml)

  for sub_dir in os.scandir(role):
    delete_empty_dirs(sub_dir.path)
      
def clean_dir(dir: str, skip_roles):
    roles_path = dir + "/roles"
    if not skip_roles and os.path.isdir(roles_path):
        for role in os.scandir(roles_path):
            clean_role(role.path)
    
    delete_empty_dirs(dir)

    

    

    