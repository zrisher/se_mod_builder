import os
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from src import __version__, tasks
from src.lib.config import load_global_config, load_project_config


DESCRIPTION = """
Provides tasks to help build and deploy Space Engineers mods.

example-config
Generates an example build.yml config file in SRC.

pre-build
Updates the VersionInfo for your solution with a revision number from git.

post-build
Builds models.
Distributes steam assets and scripts to mods folder.
Kills SE & Arms Loader processes.
Distributes to arms loader, publishing if env == 'release'.
Starts SE unless env == 'release'.
"""
INSTALL_DIR = os.path.dirname(os.path.realpath(
    sys.executable if sys.frozen else __file__
))


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
        'task',
        choices=['example-config', 'post-build', 'pre-build'],
        help='the task to run, see above',
        metavar='TASK',
    )
    parser.add_argument(
        '-e', '--env',
        help='the environment being built, defaults to "debug"',
        default='debug',
    )
    parser.add_argument(
        '-s', '--src',
        help='path to source dir, defaults to cwd',
        default=os.getcwd(),
    )

    args = parser.parse_args()
    env = args.env
    src = os.path.realpath(args.src)
    task = args.task

    print(' ----- SE Mod Builder {} doing {} ----- '.format(__version__, task))
    global_config = load_global_config(INSTALL_DIR)

    if task == 'example-config':
        tasks.gen_example_project_config(global_config, src)
    elif task == 'post-build':
        project_config = load_project_config(src, global_config)
        tasks.post_build(global_config, project_config, env)
    elif task == 'pre-build':
        project_config = load_project_config(src, global_config)
        tasks.pre_build(global_config, project_config)

    # return exit code OK
    print(' ----- SE Mod Builder finished {} ----- '.format(task))
    return 0


if __name__ == '__main__':
    sys.exit(main())
