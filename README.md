[![CI](https://github.com/lpenz/disk-img-tool/actions/workflows/ci.yml/badge.svg)](https://github.com/lpenz/disk-img-tool/actions/workflows/ci.yml)
[![docs](https://readthedocs.org/projects/disk-img-tool/badge/?version=latest)](https://disk-img-tool.readthedocs.io/en/latest/?badge=latest)
[![coveralls](https://coveralls.io/repos/github/lpenz/disk-img-tool/badge.svg?branch=main)](https://coveralls.io/github/lpenz/disk-img-tool?branch=main)
[![PyPI](https://img.shields.io/pypi/v/disk-img-tool)](https://pypi.org/project/disk-img-tool/)
[![github](https://img.shields.io/github/v/release/lpenz/disk-img-tool?logo=github)](https://github.com/lpenz/disk-img-tool/releases)


# disk-img-tool

**disk-img-tool** can be used to resize, list/get/put files and shell
into raw disk images, including Raspberry Pi OS release and other
Linux releases.


## Usage

- `disk-img-tool [-v] *image* list`

  List all files in image

- `disk-img-tool [-v] *image* enter`

  Start a shell inside the image

- `disk-img-tool [-v] *image* get *source* *dest*`

  Get a file *source* from the image and write it to *dest* in the
  outer filesystem.

- `disk-img-tool [-v] *image* put *source* *dest*`

  Put a file *source* from the outer filesystem into the image,
  writing it to the path *dest*.


## Examples using the Raspberry Pi OS image

For the sake of having an example, we can download one of the
installation images from the
[Raspbery Pi download page](https://www.raspberrypi.com/software/operating-systems)
and decompress it with `xz -d raspios-bullseye-arm64.img.xz`. That
leaves us with a *raspios-bullseye-arm64.img* file that we can then
use with the commands below.

In fact, the Raspberry Pi OS supports the injection of a `custom.toml`
file into its installation media which allows us to define the
hostname, initial user with ssh public keys, wlan configuration,
etc. Here's a sample with more documentation: [`custom.toml`]

Note: most of these need *sudo* to work due to the need to *mount*
directories. We can use the `-v` flag before the image name to ask the
tool to print all commands used.

- List files in the image's inner filesystem:
  ```sh
  $ sudo disk-img-tool raspio-bullseye-arm64.img list
        661      4 -rw-r--r--   1 root     root           12 May  3 03:53 ./etc/hostname
  ...
  ```
- "Enter" the image - i.e. mount its filesystem, chroot to it and start a shell:
  ```
  $ sudo disk-img-tool -v raspio-bullseye-arm64.img enter
  diskimgtool: + kpartx -a -v raspio-bullseye-arm64.img
  diskimgtool:   add map loop0p1 (254:0): 0 524288 linear 7:0 8192
  diskimgtool:   add map loop0p2 (254:1): 0 3571712 linear 7:0 532480
  diskimgtool: + mount -t auto /dev/mapper/loop0p2 $PWD/tmp1vxc8gvg
  diskimgtool: + mount -t auto /dev/mapper/loop0p1 $PWD/tmp1vxc8gvg/boot
  diskimgtool: + mount -t devtmpfs dev $PWD/tmp1vxc8gvg/dev
  diskimgtool: + mount -t devpts devpts $PWD/tmp1vxc8gvg/dev/pts
  diskimgtool: + mount -t tmpfs tmpfs $PWD/tmp1vxc8gvg/dev/shm
  diskimgtool: + mount -t proc proc $PWD/tmp1vxc8gvg/proc
  diskimgtool: + mount -t sysfs sysfs $PWD/tmp1vxc8gvg/sys
  diskimgtool: + mount -t tmpfs tmpfs $PWD/tmp1vxc8gvg/run
  diskimgtool: + mkdir -p $PWD/tmp1vxc8gvg/run/lock $PWD/tmp1vxc8gvg/run/shm
  diskimgtool: + chroot $PWD/tmp1vxc8gvg /bin/bash -i
  root@raspberrypi:/#
  ```
  (depends on proper qemu configuration)
- Get a file from the image's inner filesystem:
  ```
  $ sudo disk-img-tool -v raspio-bullseye-arm64.img get /etc/hostname hostname
  diskimgtool: + kpartx -a -v raspio-bullseye-arm64.img
  diskimgtool:   add map loop0p1 (254:0): 0 524288 linear 7:0 8192
  diskimgtool:   add map loop0p2 (254:1): 0 3571712 linear 7:0 532480
  diskimgtool: + mount -t auto /dev/mapper/loop0p2 $PWD/tmp6e21wrf3
  diskimgtool: + mount -t auto /dev/mapper/loop0p1 $PWD/tmp6e21wrf3/boot
  diskimgtool: Getting /etc/hostname from image as hostname
  diskimgtool: + umount $PWD/tmp6e21wrf3/boot
  diskimgtool: + umount $PWD/tmp6e21wrf3
  diskimgtool: + kpartx -d raspio-bullseye-arm64.img
  diskimgtool: + sync
  ```
- Put a file in the image's inner filesystem:
  ```
  $ sudo disk-img-tool -v raspio-bullseye-arm64.img put custom.toml /boot/
  ```


## Installation


### Releases

disk-img-tool can be installed via [pypi]:

```
pip install disk-img-tool
```

For [nix] users, it is also available as a [flake].


### Repository

We can also clone the github repository and install disk-img-tool from it with:

```
pip install .
```

We can also install it for the current user only by running instead:

```
pip install --user .
```


## Development

disk-img-tool uses the standard python3 infra. To develop and test the module:
- Clone the repository and go into the directory:
  ```
  git clone git@github.com:lpenz/disk-img-tool.git
  cd disk-img-tool
  ```
- Use [`venv`] to create a local virtual environment with
  ```
  python -m venv venv
  ```
- Activate the environment by running the shell-specific `activate`
  script in `./venv/bin/`. For [fish], for instance, run:
  ```
  source ./venv/bin/activate.fish
  ```
- Install disk-img-tool in "editable mode":
  ```
  pip install -e '.[test]'
  ```
- To run the tests:
  ```
  pytest
  ```
  Or, to run the tests with coverage:
  ```
  pytest --cov
  ```
- To generate the documentaion:
  ```
  pip install -r docs/requirements.txt
  sphinx-build -b html docs/ _docs
  ```
  And open *_docs/index.html* in a browser.
- Finally, to exit the environment and clean it up:
  ```
  deactivate
  rm -rf venv
  ```


[pypi]: https://pypi.org/project/disk-img-tool/
[nix]: https://nixos.org/
[flake]: https://nixos.wiki/wiki/Flakes
[`venv`]: https://docs.python.org/3/library/venv.html
[`custom.toml`]: https://gist.github.com/lpenz/ef21bb38a7aa12ebde17fa719a8546b5
