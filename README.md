# Ansible Collection - nixargh.ansible

<!-- vim-markdown-toc GitLab -->

* [Description](#description)
* [Roles](#roles)
* [Usage](#usage)
    * [Add collection to requirements](#add-collection-to-requirements)
    * [Install requirements](#install-requirements)
    * [Use role](#use-role)

<!-- vim-markdown-toc -->

## Description

A set of Ansible roles I created for my own use, which I don't mind to share with anyone.

## Roles

- `geesefs`: the role to FUSE mount S3 buckets using [GeeseFS](https://github.com/yandex-cloud/geesefs).
- `duplicity`: only installation tasks as it hasn't goes further ([Duplicity](https://duplicity.gitlab.io/docs.html) site).
- `timers`: the role to create systemd services and timers from a single dict of parameters.
- `warp`: the role to install and configure [Cloudflare WARP](https://developers.cloudflare.com/warp-client/get-started/linux/) software.
- `whereamifrom`: the role to configure systemd unit that runs [whereamifrom](https://crates.io/crates/whereamifrom) daemon. Installation of binary is optional via Cargo.
- `k9s`: the role to install and configure [k9s](https://k9scli.io/) utility.
- `xlibre`: switch to [XLibre Xserver](https://github.com/X11Libre/xserver?tab=readme-ov-file).
- `teamspeak`: a server and client for audio communication application - [TeamSpeak](https://www.teamspeak.com/en/).

## Usage

Let's take `warp` role for example.

### Add collection to requirements

`requirements.yaml`:
```yaml
---
collections:
  - name: nixargh.ansible
    version: main
    type: git
    source: https://github.com/nixargh/ansible.git
```

### Install requirements

```bash
ansible-galaxy collection install -r ./requirements.yaml --force
```

### Use role

`playbook.yaml`:
```yaml
---
- name: Configure Desktops
  hosts:
    - your_desktop
  collections:
    - nixargh.ansible
  roles:
    - warp
  vars:
    # replace with yours or leave empty if you don't need settings override
    warp_organization: GNU
```
