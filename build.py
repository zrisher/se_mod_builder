# run.py
#
# This script combines the individual module folders into a single structure
# for Space Engineers to load (and a bunch of other useful deploy tasks)
#
# We expect SEModHelpers to live one level below the top-level source folder
#
# It will create two mods,
#   "%AppData%\SpaceEngineers\Mods\ModName" and
#   "%AppData%\SpaceEngineers\Mods\ModName Dev".
#
# The Dev version has logging enabled

import os
import os.path
import sys



import lib

import re


def build_distro():
    print("\n\n------- SEModHelpers Python Build Script  -------\n")

    # === Get Build Script paths

    build_script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    print("Running from " + build_script_dir)
    build_model_path = os.path.join(build_script_dir, 'build_model.py')

    build_config_path = lib.paths.find_file_up(
        "build_config.yml", build_script_dir, 4
    )
    if build_config_path:
        print("Config file found at " + build_config_path)
    else:
        print("build_config.yml is missing. Aborting script.")
        return

    # === Load config

    print("\n----- Config -----\n")

    config = lib.config.load(build_config_path)
    if not config:
        return

    source_modules = config['source_modules']
    distributions = config['distributions']
    mwm_builder_path = config['mwm_builder_path']

    print("Source Modules: ")
    for module_name, module_path in source_modules.items():
        print(" - " + module_name + ": " + module_path)
    print("")

    print("Distributions")
    for dist_key, dist_config in distributions.items():
        print(" - " + dist_key + ": ")
        #for k,v in dist_config.items():
        #    print("     {0}: {1}".format(k, v))
        print("     {0}: {1}".format('Path', dist_config['path']))
        print("     {0}: {1}".format('cleanup_ignores', dist_config['cleanup_ignores']))
        print("     {0}: {1}".format('compile_symbols_to_remove', dist_config['compile_symbols_to_remove']))
    print("")

    print("MWM Builder Path: " + mwm_builder_path)
    print("")

    # === Run Build

    print("----- Running Build ----- \n")

    # Start MWM Builder, which runs in parallel
    print("--- Starting MWM Model Builder Threads --- ")
    mwm_processes = lib.build.process_models(
        source_modules, build_model_path, mwm_builder_path
    )
    mwm_processes_count = mwm_processes.__len__()
    if mwm_processes_count > 0:
        print("Running {0} mwm_processes.".format(mwm_processes.__len__()))
    else:
        print("no mwm_processes running")
    print("")

    # Clean Destinations
    print("--- Cleaning Dist Dirs ---")
    lib.build.clean_distributions(distributions)
    print("")

    # Copy Data
    print("--- Copying Data ---")
    lib.build.distribute(source_modules, distributions, [["Data"]], "sbc")
    print("")

    # Copy Scripts
    print("--- Copying Scripts ---")
    lib.build.distribute(source_modules, distributions,
                     [["Scripts"],["Data", "Scripts"]], "cs",
                     dist_content_path = ["Data", "Scripts"],
                     squash_modules=False)  # , squash_dirs=True)
    print("")

    # Copy Textures
    print(" --- Copying Textures --- ")
    lib.build.distribute(source_modules, distributions, [["Textures"]], "dds")
    print("\n")


    # Copy Models once they're built
    if mwm_processes_count > 0:
        print("waiting for our mwm processes to finish")
        for mwm_process in mwm_processes:
            mwm_process.wait()

    print(" --- Distributing Models --- ")
    lib.build.distribute(source_modules, distributions, [["Model"]], "mwm")
    print("\n")


    print("------- SEModHelpers Python Build Complete  ------- \n")


if __name__ == '__main__':
    build_distro()