import os
from datetime import datetime
from ..common import get_template 

DEFAULT_DIR = "./"
TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/templates'

def render_file_template(parent, src: str, dest: str, config: dict):
    full_path = parent + '/' + dest
    template = get_template(src, TEMPLATE_DIR)
    config.update({'date': datetime.now()})
    content = template.render(config)
    with open(full_path, 'w') as file:
        file.write(content)

def init_def(dir: str, config: dict):
    if dir != DEFAULT_DIR:
        os.makedirs(dir, exist_ok=True)

    render_file_template(dir, f"execution-environment-v{config['version']}.yml.j2", "execution-environment.yml", config)
