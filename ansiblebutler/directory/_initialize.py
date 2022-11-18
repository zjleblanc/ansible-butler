import os
import yaml
from jinja2 import Environment, Template, FileSystemLoader
from datetime import datetime

DEFAULT_DIR = "./"
TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/templates'

with open(TEMPLATE_DIR + '/structure.yml', 'r') as stream:
    STRUCTURE = yaml.safe_load(stream)

def create_file(parent, file: str):
    full_path = parent + '/' + file
    if file.endswith('.j2'):
        environment = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
        template = environment.get_template(file)
        content = template.render({'date': datetime.now()})
        with open(full_path[:-3], 'w') as file:
            file.write(content)
    else:
        with open(full_path, 'a'):
            os.utime(full_path, None)

def create_folder(parent, folder):
    for file in folder.get('files', []):
        create_file(parent, file)
    
    for folder in folder.get('folders', []):
        path = parent + '/' + folder['name']
        os.makedirs(path, exist_ok=True)
        create_folder(path, folder)

def init_dir(dir: str):
    if dir != DEFAULT_DIR:
        os.makedirs(dir, exist_ok=True)
    create_folder(dir, STRUCTURE)

  
