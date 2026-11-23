# yc_cli

Installs a pinned [Yandex Cloud CLI](https://yandex.cloud/en/docs/cli/operations/install-cli)
binary from Yandex Cloud Object Storage.
Supports Linux on x86_64 and aarch64, including Ubuntu.

```yaml
---
- name: Install Yandex Cloud CLI on workstations
  hosts: workstations
  roles:
    - nixargh.ansible.yc_cli
```

The installation tasks use privilege escalation. Pass `-K` if sudo prompts
for a password.

Run the role selectively with `ansible-playbook playbook.yaml --tags yc_cli`.
The `yc_cli_install` tag selects the same installation tasks.

The role stores versioned binaries in `yc_cli_binary_dir` (default
`/usr/local/lib/yc-cli`) and manages a symlink at `yc_cli_install_path`
(default `/usr/local/bin/yc`). If a regular file already occupies the link
path, move it aside before using the role. When overriding the link path,
use an absolute path with an existing parent directory.

Set `yc_cli_version` to install a different release. Previous binaries
remain available for rollback by selecting their version again.

Run `yc init` as the workstation user to configure their own CLI profile.
