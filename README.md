# Space Engineers Mod Builder

Space Engineers Mod Builder (SEMB) is a simple program and set of conventions
that allow users to easily build, distribute, and release Space Engineers mods.

SEMB works with both normal mod content distributed through Steam as well as
plugins distributed through 
[Space Engineers Plugin Loader](https://github.com/Rynchodon/SEPL) (SEPL).

SEMB provides tasks that:
* Place a git-based revision number in the assembly version (for SEPL)
* Build model `.mwm` files
* Distribute steam assets to the SE mods folder.
* Start and stop SE processes (for SEPL)

These tasks can be easily attached to your Visual Studio build events.


## Requirements
* Space Engineers
* If you'd like to build SEPL plugins:
    * [Git](https://git-scm.com/downloads) - for releasing and versioning
    * [SE Plugin Loader](https://github.com/Rynchodon/SEPL) -
    ensure you've installed and configured it, including:
       * set the Steam plugin flag 
       * provide a local git with oAuth
       * create an appropriate config file within your project

* If you'd like to build SEMB from source:
  * [Conda](https://conda.io/docs/)


## Installation

### Installing a pre-built release
Simply download the latest release from 
[the releases page](https://github.com/zrisher/se_mod_builder/releases).
Extract the executable somewhere and add its folder to your path.

### Building from source
* Fork and clone the repo
* Run `conda env create` to create the environment
* Run `conda activate se_mod_builder` to load the environment
* Run `python se_mod_builder.py args` to use it via python
* Run `pyinstaller se_mod_builder.spec` to generate the executable
* Add the executable to your path


## Configuration

### Global
If you have non-standard paths to Git or SE, run

```
SEModBuilder example-global-config
```

to generate an example `config.yml` global config file in its install dir. 

Edit it to provide any changes specific to your project.

### Project
If you have non-standard paths to mod assets within your project, run 

```
SEModBuilder example-project-config
```

from your project root 
to generate an example `build.yml` project config file there. 

Edit it to provide any changes specific to your project.


## Usage
SEMB provides many tasks to assist with building your project. Run

```
SEModBuilder --help
```

to see a list of all of them and what they do.

If you have issues with a particular command, try adding the `--debug` flag.

### Visual Studio example

For a full project with both Steam and SEPL assets, your build events might be:


#### pre-build

```
SEModBuilder git-version
```

#### post-build

```
SEModBuilder kill-se
SEModBuilder build-models
SEModBuilder distribute-steam

if $(ConfigurationName) == release ( 
  PluginManager ..\..\..\..\..\plugin.json publish=True
) else (
  PluginManager ..\..\..\..\..\plugin.json 
  SEModBuilder start-se
)
```

## Contributing
Contributions are welcome! 

Maintain your development branches on your own fork and submit PRs when ready.

Run tests and linting with `pytest --pep8`.
