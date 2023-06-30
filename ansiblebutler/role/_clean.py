import os
import glob
from ..common import load_yml

def clean_role(role: str):
  for yml in glob.glob(role + "/**/*.yml"):
    if not load_yml(yml):
      os.remove(yml)

  for _dir in os.scandir(role):
    if os.path.isdir(_dir) and not os.listdir(_dir):
      os.rmdir(_dir)