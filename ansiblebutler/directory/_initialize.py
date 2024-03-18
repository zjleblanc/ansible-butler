import os
import json
import shutil
from ..common import get_template 
from datetime import datetime

DEFAULT_DIR = "./"
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__)) + '/configs'
TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/templates'

def create_file(parent, file: str, config={'date': datetime.now()}):
    full_path = parent + '/' + file

    # Handle jinja template
    if file.endswith('.j2'):
        dest = full_path[:-3]
        if os.path.isfile(dest):
            print(f"Skipping {dest}: file already exists")
            return
        template = get_template(file, TEMPLATE_DIR)
        content = template.render(config)
        with open(dest, 'w') as file:
            file.write(content)
        return
    
    if os.path.isfile(full_path):
        print(f"Skipping {full_path}: file already exists")
        return
    with open(full_path, 'a'):
        os.utime(full_path, None)

def create_folder(parent, folder):
    for file in folder.get('files', []):
        create_file(parent, file)
    
    for folder in folder.get('folders', []):
        path = parent + '/' + folder['name']
        if os.path.isdir(path):
            print(f"Skipping {path}: folder already exists")
            return
        os.makedirs(path, exist_ok=True)
        create_folder(path, folder)

def create_lint(dir: str, file: str):
    src = CONFIG_DIR + '/.ansible-lint'
    dest = dir + '/' + file
    shutil.copyfile(src, dest)

def create_code_bot(dir: str, config: dict):
    path = dir + '/.github/ansible-code-bot.yml'
    if os.path.isfile(path):
        print ("Skipping codebot: config already exists.")
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    create_file(dir, '/.github/ansible-code-bot.yml.j2', config)

def create_vscode(dir: str, config: dict):
    settings = config['settings']
    path = dir + '/.vscode/settings.json'
    # Read existing settings
    if os.path.isfile(path):
        with open(path) as fd:
            existing = json.load(fd)
            settings.update(existing)
    # Write udpated settings
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as fd:
        fd.write(json.dumps(settings, indent=4))

def init_dir(dir: str, config: dict):
    if dir != DEFAULT_DIR:
        os.makedirs(dir, exist_ok=True)
    create_folder(dir, config)
    
    if config['lint']['enabled']:
        create_lint(dir, '.ansible-lint')
    if config['code_bot']['enabled']:
        create_code_bot(dir, config['code_bot'])
    if config['vscode']['enabled']:
        create_vscode(dir, config['vscode'])