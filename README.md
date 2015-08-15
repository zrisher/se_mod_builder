# SE Mod Helpers - Build Script
This script assists with the deployment of Space Engineers mods from their
source/development locations to the SE mods directory for testing and
publishing.

## Requirements
* Python 2.7 or greater

## Installation
* Include SEModHelpers as a submodule into your repo, as per its install guide.
* Copy build_config.yml.example to the top-level directory of your mod
* Remove the ".example" from its name and fill in your own configuration details

## Usage
Double-click *build.bat* in the SEModHelpers folder, or run
 `python Path/To/SEModHelpers/.build/build.py`.

### File Structure
The build script can work with either a module-based structure or a flat one,
but either way we expect the *Script* dir to **not** be contained within data.

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
    - Models
    - Scripts
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


