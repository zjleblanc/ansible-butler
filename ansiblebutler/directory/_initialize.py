import os
from ..common import get_template 
from datetime import datetime

DEFAULT_DIR = "./"
TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/templates'

def create_file(parent, file: str):
    full_path = parent + '/' + file
    if file.endswith('.j2'):
        template = get_template(file, TEMPLATE_DIR)
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

def init_dir(dir: str, structure: dict):
    if dir != DEFAULT_DIR:
        os.makedirs(dir, exist_ok=True)
    create_folder(dir, structure)

  
