# SE Mod Builder
This package assists with the deployment of Space Engineers mods. 

It provides for basic SE mod deployment:
* Runs SE asset building tasks (Mwm Builder)
* Deploys all assets and code distributed through Steam to the SE mods dir

As well as for deploying with [SE Plugin Loader](https://github.com/Rynchodon/SEPL):
* Places git-based revision number in the assembly version
* Stops SE (and thus SEPL) before running SEPL
* Runs deployment and release tasks via SEPL
* Restarts SE

Once you have installed SE Mod Builder and configured your project, 
you will be able to launch it in SE for development or release it to users by 
simply selecting your configuration in Visual Studio and clicking "Build".


## Requirements
* [Git](https://git-scm.com/downloads) - for releasing and versioning
* [SE Plugin Loader](https://github.com/Rynchodon/SEPL) - 
ensure you've installed and configured it following the readme,
including setting the Steam plugin flag 
and providing a local oAuth token for git.
* [Conda](https://conda.io/docs/) - if you'd like to build SEMB from source


## Installation

##### Installing a pre-build release
Simply download and run the latest installer from [the releases page](https://github.com/zrisher/se_mod_builder/releases).

##### Building from source
* Fork and clone the repo
* Run `conda env create` to create the environment
* Run `conda activate se_mod_builder` to load the environment
* Run `python se_mod_builder.py args` to use it via python
* Run `pyinstaller se_mod_builder.spec` to generate the executable
* Add the executable to your path


## Configuration

##### Global
If you have non-standard paths to Git or SE, copy `config.example.yml` to
`config.yml` in SE Mod Builder's install directory and edit it to provide 
your paths.

##### Project
Run `se_mod_builder example-config` from your project root to generate an 
example `build.yml` project config file there. 
Edit it to provide any changes specific to your project.

##### Visual Studio
For each project in your solution, set the pre-build event to:

`se_mod_builder pre-build --src="../to/proj/root" --env $(ConfigurationName)`

And the post-build event to:

`se_mod_builder post-build --src="../to/proj/root" --env $(ConfigurationName)`


## Usage

##### Developing
Simply edit your code and assets, set your configuration to anything besides
`release`, and click "Build" to deploy all changes. 
SE will start automatically when finished deploying.

##### Releasing
When your code is ready to release:
 * Bump the version in Properties/VersionInfo and commit.
 * Push your code to github and ensure it's merged into master.
 * Change your build to "release" and click "Build". This will publish your
 changes to SEPL.
 * If you've changed your steam-shipped code, publish it using SE.


## Contributing
Contributions are welcome! 
Maintain your development branches on your own fork and submit PRs when ready.

Run tests and linting with `pytest --pep8`.
