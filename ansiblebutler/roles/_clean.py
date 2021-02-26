import os
import glob
from ._common import parse_yml

def clean_role(role: str):
  for yml in glob.glob(role + "/**/*.yml"):
    if not parse_yml(yml):
      os.remove(yml)

  for _dir in os.scandir(role):
    if os.path.isdir(_dir) and not os.listdir(_dir):
      os.rmdir(_dir)