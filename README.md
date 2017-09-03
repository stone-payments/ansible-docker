stone-payments.docker
============
This Ansible role will setup and configure a Docker service on a RHEL-like (CentOS, Fedora also supported) system.
There's also support for enabling some workarounds to improve Docker stability.

So far, there's only support for "direct-lvm" storage backend, where a whole block device is dedicated to store the
container images. This is a production-ready storage backend to use, and it's the most stable one with very good
performance, with the drawback of increased memory usage.

## Usage
You **must** have a dedicated block device for the role to create a LVM PV, VG and setup the needed LVs on it.
The intended device should be passed as a variable to the role, but the role will check if there's already some
filesystem signature on it and abort if that's the case (set `docker_vg.create` to `true` to force overwriting).

Here's an example playbook:
```yaml
- name: configure docker
  hosts: all
  become: true
  roles:
    - stone-payments.docker
  vars:
    docker_vg: #this whole dict may be omitted if you intend to use the default "/dev/sdb"
      name: docker #purely informative, but there should be a name
      create: false #wipe devices listed on docker_vg.devs
      devs: #you may use more than a single block device here if needed, they will be joined to create a VG
        - "/dev/sdb"
```

## Advanced settings
In the `defaults\main.yml` file you may find advanced settings to fine-tune the role to your environment. The available
options include:
* Docker version to use (must be available on the system);
* TLS configuration of the Docker API socket;
* Fraction of available space to use for container images and for container-generated data;
* Enable/disable workarounds of some Docker bugs;
* Enable/disable some Docker plugins (so far, only support for RHEL registry plugin);
* Custom configs that should be passed directly to `/etc/docker/daemon.json` config file.

## Contributing
Just open a PR! We love PRs.

## License
This role is distributed under the MIT license.
