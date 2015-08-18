# SE Mod Helpers - Build Script
This script assists with the deployment of Space Engineers mods from their
source/development locations to the SE mods directory for testing and
publishing.

## Requirements
* Python 2.7 or greater
* Conda (Miniconda or Anaconda)

** When we deploy this to an exe the above requirements will be removed. **

## Installation
* Copy build_config.example.yml to the top-level directory of your mod
* Remove the ".example" from its name and fill in your own configuration details
* Run `conda env create` in the se_mod_builder dir

## Usage
```
cd Path/To/se_mod_builder
activate se_mod_builder
python build.py path/to/mod_source
```

### File Structure
The build script can work with either a module-based structure or a flat one.

A fully-deployed SE mod will have the file structure:

  ModName
    - Data
        - Scripts
            - *.cs
        - *.sbc
    - Models
        - ... various levels and folders ...
            - *.mwm
    - Textures
        - ... various levels and folders ...
            - *.dds

With this script, you can use either:

  ModName
    - Data
        - Scripts
    - Models
    - Textures

Or (using config option has_modules = true):

  ModSourceFolder
    - Module1
        - Data
        - Scripts
        - Textures
    - Module2
        - Data
        - Textures
    ... etc ...


