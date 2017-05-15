import os
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from src import __version__, tasks
from src.lib import logging, config

if hasattr(sys, 'frozen'):
    INSTALL_DIR = os.path.dirname(os.path.realpath(sys.executable))
    ASSET_DIR = sys._MEIPASS
else:
    INSTALL_DIR = ASSET_DIR = os.path.dirname(os.path.realpath(__file__))

DESCRIPTION = """
==== SE Mod Builder ====
Provides tasks to help build and deploy Space Engineers mods.
All commands besides "example-config" should be run from a build event script.

example-global-config
Create an example config.yml in SEMB's install directory.

example-project-config
Create an example build.yml at CWD. Should be run from project root.

git-version
Updates the VersionInfo for your solution with a revision number from git.
Should be run before compilation so the version is included in your assembly.

build-models
Generates .mwm files from sources. Should be run before distribution.

distribute-steam
Copy all assets published through Steam to the SE mod folder.
Also removes any outdated files from its distribution paths.

kill-se
Stop and wait for exit of all SE processes, including SE Plugin Loader.
This is useful for SEPL plugins, which are loaded into the SE process.

start-se
Start the SE client. SEPL should be attached with the "plugin" option.
"""


def main():
    """
    Parses provided args and runs specified task
    """
    parser = ArgumentParser(
        description=DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=__version__
    )
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='output additional detail, default False',
    )
    parser.add_argument(
        'task',
        choices=[
            'build-models', 'distribute-steam',
            'example-global-config', 'example-project-config',
            'git-version', 'kill-se', 'start-se'
        ],
        help='the task to run, see above',
        metavar='TASK',
    )
    parser.add_argument(
        '-r', '--root',
        help='path to project root, defaults to "..\..\..\..\.."',
        default='..\..\..\..\..'
    )

    args = parser.parse_args()
    logging.Verbose = args.debug
    project_dir = os.path.realpath(args.root)
    task = args.task

    print(' ----- SE Mod Builder {} doing {} ----- '.format(__version__, task))
    do_task(args.task, project_dir)
    print(' ----- SE Mod Builder finished {} ----- '.format(task))
    return 0


def do_task(task, project_dir):
    if task == 'example-global-config':
        tasks.example_global_config(ASSET_DIR, INSTALL_DIR)
        return

    if task == 'example-project-config':
        tasks.example_project_config(ASSET_DIR, os.getcwd())
        return

    global_config = config.load_global_config(INSTALL_DIR)
    project_config = config.load_project_config(project_dir)

    if task == 'build-models':
        tasks.build_models(global_config, project_config)
    elif task == 'distribute-steam':
        tasks.distribute_steam(global_config, project_config)
    elif task == 'git-version':
        tasks.git_version(global_config, project_config)
    elif task == 'kill-se':
        tasks.kill_se(global_config, project_config)
    elif task == 'start-se':
        tasks.start_se(global_config, project_config)


if __name__ == '__main__':
    sys.exit(main())
