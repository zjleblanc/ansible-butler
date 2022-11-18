ansible-butler
=========

Butler CLI for Ansible projects

Functions
------------

| Object | Action | Description |
| ------ | ------ | ----------- |
| directory | init | initialize an ansible directory |
| directory | init | cleanup an ansible directory |
| role | list | list roles |
| role | clean | clean role directory structure (remove empty yml files & dirs) |
| role | mk-readme | auto generate readme based on role meta and basic yml info |

Usage
--------------

```
Usage:
  ansible-butler directory init [<dir>]
  ansible-butler directory clean [<dir>] [--skip-roles]
  ansible-butler role list [--roles-path=PATH] [<name>]
  ansible-butler role clean [--roles-path=PATH] [<name>]
  ansible-butler role mk-readme [--roles-path=PATH] [<name>]

Arguments:
  name    name of role (accepts glob patterns)
  dir     path to directory [default: ./]

Options:
  -h --help                               Show this screen
  --roles-path=PATH   Path to roles directory [default: ./roles]
  --skip-roles        Flag to skip cleaning roles
```

Examples
----------------

- Initialize Ansible Directory
  - `ansible-butler directory init ./sandbox`
- Clean an Ansible Directory
  - `ansible-butler directory clean ./sandbox`
  - `ansible-butler directory clean ./sandbox --skip-roles`
- Clean Roles 
  - `ansible-butler role clean my-role-1`
  - `ansible-butler role clean my-role-*`
- Generate README
  - `ansible-butler role mk-readme my-role-1`
  - `ansible-butler role mk-readme my-role-*`

Troubleshooting
----------------

- `ansible-butler: command not found`
  - check the $PATH environment variable and ensure that `~/.local/bin` is included

License
-------

GNU General Public License

Author Information
-------
**Zach LeBlanc**

Red Hat