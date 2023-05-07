ansible-butler
=========

Butler CLI for Ansible projects

Functions
------------

| Object | Action | Description |
| ------ | ------ | ----------- |
| directory | init | initialize an ansible directory |
| directory | init | cleanup an ansible directory |
| ee | init | initialize an execution environment directory for ansible-builder |
| role | list | list roles |
| role | clean | clean role directory structure (remove empty yml files & dirs) |
| role | mk-readme | auto generate readme based on role meta and basic yml info |

Usage
--------------

```
Usage:
  ansible-butler directory init [<dir>] [--config=PATH]
  ansible-butler directory clean [<dir>] [--skip-roles]
  ansible-butler ee init [<dir>] [--config=PATH]
  ansible-butler role list [--roles-path=PATH] [<name>]
  ansible-butler role clean [--roles-path=PATH] [<name>]
  ansible-butler role mk-readme [--roles-path=PATH] [<name>]

Arguments:
  name    name of role (accepts glob patterns)
  dir     path to directory [default: ./]

Options:
  -h --help           Show this screen
  --config=PATH       Path to config file
  --roles-path=PATH   Path to roles directory [default: ./roles]
  --skip-roles        Flag to skip cleaning roles
```

Examples
----------------

- Initialize Ansible Directory
  - `ansible-butler directory init ./sandbox`
  - `ansible-butler directory init ./sandbox --config=~/configs/ansible-butler.yml`
- Clean an Ansible Directory
  - `ansible-butler directory clean ./sandbox`
  - `ansible-butler directory clean ./sandbox --skip-roles`
- Initialize Execution Environment Directory
  - `ansible-butler ee init ./ee-windows`
  - `ansible-butler ee init ./ee-windows --config=~/configs/ansible-butler.yml`
- Clean Roles 
  - `ansible-butler role clean my-role-1`
  - `ansible-butler role clean my-role-*`
- Generate README
  - `ansible-butler role mk-readme my-role-1`
  - `ansible-butler role mk-readme my-role-*`

Configuration
-------------

Create an `.ansible-butler.yml` in one or more of the following locations:
```
/etc/ansible-butler/    ## least precedence
~/
./                      ## highest precedence
```

You can also specify a specific path at runtime via the `--config` option.

```yaml
# Configuration Schema
execution_environment:
  init:
    version: 2
    ansible_config: ansible.cfg
    ee_base_image: quay.io/ansible/ansible-runner:latest
    ee_builder_image: quay.io/ansible/ansible-builder:latest
    prepend_build_steps:
      - ...
    append_build_steps:
      - ...
directory:
  init:
    folders:
      - name: plugins
        folders:
          ...
        files:
          - README.md
    files:
      - playbook.yml
role: {}
```

[🔗 Default configuration file](./ansiblebutler/common/.ansible-butler.yml)
<br>
[🔗 Example adding test plugins directory](./docs/config/.ansible-butler.test-plugins.yml)

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