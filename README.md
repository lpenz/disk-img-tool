[![CI](https://github.com/lpenz/disk-img-tool/actions/workflows/ci.yml/badge.svg)](https://github.com/lpenz/disk-img-tool/actions/workflows/ci.yml)
[![coveralls](https://coveralls.io/repos/github/lpenz/disk-img-tool/badge.svg?branch=main)](https://coveralls.io/github/lpenz/disk-img-tool?branch=main)
[![PyPI](https://img.shields.io/pypi/v/disk-img-tool)](https://pypi.org/project/disk-img-tool/)
[![github](https://img.shields.io/github/v/release/lpenz/disk-img-tool?logo=github)](https://github.com/lpenz/disk-img-tool/releases)


# disk-img-tool

**disk-img-tool** can be used to resize, list/get/put files and shell
into raw disk images, including Raspberry Pi OS release.


## Installation


### Releases

disk-img-tool can be installed via [pypi]:

```.sh
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
- Finally, to exit the environment and clean it up:
  ```
  deactivate
  rm -rf venv
  ```


[pypi]: https://pypi.org/project/disk-img-tool/
[nix]: https://nixos.org/
[flake]: https://nixos.wiki/wiki/Flakes
[`venv`]: https://docs.python.org/3/library/venv.html
