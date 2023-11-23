ansible-butler 
<a href="https://pypi.org/project/ansible-butler"><img align="right" src="https://img.shields.io/pypi/v/ansible-butler.svg"/></a>
=========

Butler CLI for Ansible projects

Functions
------------

| Object | Action | Description |
| ------ | ------ | ----------- |
| directory | init | initialize an ansible directory |
| directory | clean | cleanup an ansible directory |
| ee | init | initialize an execution environment directory for ansible-builder |
| ee | dependencies\[deps\] | parse the dependency tree based on execution environment definition (or collection requirements) |
| role | list | list roles |
| role | dependencies\[deps\] | Build a dependency graph between roles in a specified directory [[Example]](https://reports.autodotes.com/butler/graph.html) |
| role | clean | clean role directory structure (remove empty yml files & dirs) |
| role | mk-readme | auto generate readme based on role meta and basic yml info |
| playbook | update | map legacy module names to FQCNs |
| playbook | list-collections\[lc\] | list collections used in a playbook (following include_* directives) |

Usage
--------------

```
Usage:
  ansible-butler directory init [<dir>] [--config=PATH]
  ansible-butler directory clean [<dir>] [--skip-roles]
  ansible-butler ee init [<dir>] [--config=PATH]
  ansible-butler ee [dependencies|deps] [--config=PATH] [<name>]
  ansible-butler role list [--roles-path=PATH] [<name> --recursive]
  ansible-butler role [dependencies|deps] [--roles-path=PATH]
  ansible-butler role clean [--roles-path=PATH] [<name> --recursive]
  ansible-butler role mk-readme [--roles-path=PATH] [<name> --recursive]
  ansible-butler playbook update [--context=CONTEXT] [--config=PATH] [<name>] [--recursive] [--force]
  ansible-butler playbook [list-collections|lc] [--context=CONTEXT] [--config=PATH] [<name>] [--recursive] [--force]

Arguments:
  name    name of target (accepts glob patterns)
  dir     path to directory [default: ./]

Options:
  -h --help           Show this screen
  -r --recursive      Apply glob recursively [default: False]
  -f --force          Make file changes in place
  --config=PATH       Path to config file
  --roles-path=PATH   Path to roles directory [default: ./roles]
  --context=CONTEXT   Path to context directory [default: ./]
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
- Inspect Execution Environment Dependencies
  - `ansible-butler ee dependencies execution-environment.yml`
  - `ansible-butler ee deps requirements.yml --config=~/configs/ansible-butler.yml`
- Clean Roles 
  - `ansible-butler role clean my-role-1`
  - `ansible-butler role clean my-role-*`
- List Roles 
  - `ansible-butler role list`
  - `ansible-butler role list ansible_collections/namespace/collection/roles`
- Generate Dependency Graph 
  - `ansible-butler role deps`
  - `ansible-butler role deps ansible_collections/namespace/collection/roles`
- Generate README
  - `ansible-butler role mk-readme my-role-1`
  - `ansible-butler role mk-readme my-role-*`
- Update Playbooks
  - `ansible-butler playbook update --context=./playbooks -r`
  - `ansible-butler playbook update legacy-*.yml`
  - `ansible-butler playbook update -f`
- List Collections
  - `ansible-butler playbook list-collections --context=./playbooks -r`
  - `ansible-butler playbook lc example-playbook.yml`

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
# Example Configuration Schema
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

role:
  dependencies:
    output_fmt: html # [html,json]
    output_dest: graph.html
    include_tests: false
    master_node: role-common-setup
    initial_direction: downstream
    title: ansible-butler roles dependency graph
    title_text_color: white
    title_background_color: black
    tree_options:
      # Customize the color palette
      circleStrokeColor: '#2b8f91'
      linkStrokeColor: '#dddddd'
      closedNodeCircleColor: '#9bd3d4'
      openNodeCircleColor: white
      cyclicNodeColor: '#FF4242'
      missingNodeColor: '#CC0100'
      maxDepthNodeColor: '#FF5850'

playbook:
  update:
    modules:
      smart_device:
        redirect: zjleblanc.kasa.smart_device
      custom_module:
        redirect: company.it.custom_module
```

[🔗 Default configuration file](./ansiblebutler/common/.ansible-butler.yml)
<br>
[🔗 Example adding test plugins directory](./docs/config/.ansible-butler.test-plugins.yml)
<br>
[🔗 Example adding module redirects](./docs/config/.ansible-butler.module-redirects.yml)

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