import os
from datetime import datetime
from ..common import get_template 

DEFAULT_DIR = "./"
TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/templates'

def render_file_template(parent, file: str, config: dict):
    full_path = parent + '/' + file
    template = get_template(file, TEMPLATE_DIR)
    config.update({'date': datetime.now()})
    content = template.render(config)
    with open(full_path[:-3], 'w') as file:
        file.write(content)

def init_dir(dir: str, config: dict):
    if dir != DEFAULT_DIR:
        os.makedirs(dir, exist_ok=True)

    render_file_template(dir, 'execution-environment.yml.j2', config)
    render_file_template(dir, 'requirements.txt.j2', config)
    render_file_template(dir, 'requirements.yml.j2', config)
    render_file_template(dir, 'bindep.txt.j2', config)
