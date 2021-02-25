ansible-butler
=========

Butler CLI for Ansible projects

Functions
------------

| Object | Action | Description |
| ------ | ------ | ----------- |
| role | list | list roles |
| role | clean | clean role directory structure (remove empty yml files & dirs) |
| role | mk-readme | auto generate readme based on role meta and basic yml info |

Usage
--------------

```
  ansible-butler.py role list [--roles-path=PATH] [<name>]
  ansible-butler.py role clean [--roles-path=PATH] [<name>]
  ansible-butler.py role mk-readme [--roles-path=PATH] [<name>]

Arguments:
  name    name of role (accepts glob patterns)

Options:
  -h --help                               Show this screen
  --roles-path=PATH   Path to roles directory [default: ./roles]
```

Examples
----------------

- Clean Roles 
  - `ansible-butler role clean my-role-1`
  - `ansible-butler role clean my-role-*`
- Generate README
  - `ansible-butler role mk-readme my-role-1`
  - `ansible-butler role mk-readme my-role-*`

License
-------

GNU General Public License

Author Information
-------
**Zach LeBlanc**

Red Hat