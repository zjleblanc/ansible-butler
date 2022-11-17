import os
import yaml

DEFAULT_DIR = "./"
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

with open(BASE_PATH + '/structure.yml', 'r') as stream:
    STRUCTURE = yaml.safe_load(stream)

def create_folder(parent, folder):
    for file in folder.get('files', []):
        fname = parent + '/' + file
        with open(fname, 'a'):
                os.utime(fname, None)
    
    for folder in folder.get('folders', []):
        path = parent + '/' + folder['name']
        os.makedirs(path, exist_ok=True)
        create_folder(path, folder)

def init_dir(dir: str):
    if dir != DEFAULT_DIR:
        os.makedirs(dir, exist_ok=True)
    create_folder(dir, STRUCTURE)

  
