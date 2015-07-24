# lib/build.py
# SEModHelper Build Script
#
# The primary building methods
#

import os
import os.path
import re
import subprocess

from . import ops
from . import paths


def clean_distributions(distributions):
    """
    Erase everything in the distributions' dirs besides ignored files
    """
    for dist_key, dist in distributions.items():
        clean_dist_dir(dist['path'], dist['cleanup_ignores'])


def clean_dist_dir(dist_dir, cleanup_ignores):
    """
    Erase everything in the distribution dir besides ignored files
    """
    print("cleaning dist dir " + dist_dir)
    for root, dirs, files in os.walk(dist_dir):
        for file in files:
            if not any([re.match(ignore, file) for ignore in cleanup_ignores]):
                full_path = os.path.join(root, file)
                print("removing file " + full_path)
                os.remove(full_path)

    ops.recursive_delete_if_empty(dist_dir)


def distribute(source_modules, distributions, source_content_paths, extension,
               dist_content_path=[], squash_dirs=False, squash_modules=True):
    """
    Move files with extension `extension`
    from `source_content_paths` in `source_modules`
    to `dist_content_path` in `distributions`,
    or use `source_content_path` if `dist_content_path` is not supplied

    Optionally squash modules together into one folder
    Optionally squash all lower folders together as well
    If squashing, prepend folder names to files to guard against collisions
    """

    for module_name, module_path in source_modules.items():
        for source_content_path in source_content_paths:

            module_content_full_path = os.path.join(module_path,
                                                    *source_content_path)
            if not dist_content_path:
                dist_content_path = source_content_path

            for dist_key, dist in distributions.items():

                if squash_modules:
                    dist_content_path_full = os.path.join(dist['path'],
                                                          *dist_content_path)
                    file_prefix = module_name + "."
                else:
                    dist_content_path_full = os.path.join(
                        os.path.join(dist['path'], *dist_content_path),
                        module_name)
                    file_prefix = ""

                ops.deep_copy_files_with_extension(
                    module_content_full_path, dist_content_path_full, extension,
                    filename_prefix=file_prefix,
                    comp_sym_to_remove=dist['compile_symbols_to_remove'],
                    squash_dirs=squash_dirs
                )

def process_models(source_modules, model_process_path, mwm_path):
    """
    start mwmBuilder processes in parallel
    """

    mwm_processes = []

    if not model_process_path:
        print("build-model.py path missing, skipping process_models")
        return mwm_processes
    elif not os.path.exists(model_process_path):
        paths.investigateBadPath("build-model.py", model_process_path)
        return mwm_processes

    if not mwm_path:
        print("mwm builder path missing, skipping process_models")
    elif not os.path.exists(mwm_path):
        paths.investigateBadPath("MwmBuilder", model_process_path)
        return mwm_processes

    model_dir_names = ["Model", "Models"]
    size_dir_names = ["large", "small"]

    print("looking for model dirs to build from")
    for module_name, module_path in source_modules.items():
        for model_dir_name in model_dir_names:
            for size_dir_name in size_dir_names:
                models_path = os.path.join(
                    module_path, model_dir_name, size_dir_name
                )
                if os.path.exists(models_path):
                    print("spawning process for " + models_path)

                    mwm_processes.append(
                        subprocess.Popen(
                            ["python", model_process_path],
                            cwd=models_path, mwm_path=mwm_path
                        )
                    )


    return mwm_processes
