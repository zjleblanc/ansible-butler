import os
import glob

def list_roles(args: dict):
    roles_path = args.get('--roles-path')
    dir_glob = args.get('<glob>') or "*"
    for role in glob.glob(roles_path + "/" + dir_glob):
        if os.path.isdir(role):
            print(os.path.basename(role))