import os.path

import re
import yaml

from . import paths

def load(config_file_path):
    """
    Load config from a provided YAML file,
    clean it up and ensure all necessary info is available
    If so, return a dictionary with the useful info
    If not, return False
    """
    config = yaml.load(open(config_file_path, 'r'))

    # source
    source_dir = config.get('source_dir')
    source_dir = source_dir if source_dir else os.path.dirname(config_file_path)

    mod_name = config.get('mod_name')
    mod_name = mod_name if mod_name else os.path.basename(source_dir)

    if config.get('has_modules'):
        source_modules = paths.modules(source_dir)
    else:
        source_modules = {}
        source_modules[mod_name] = source_dir

    # distributions
    se_mods_dir = config.get('se_mods_dir')
    if not se_mods_dir:
        se_mods_dir = os.path.join(
            os.getenv('APPDATA'), "SpaceEngineers", "Mods"
        )

    distributions = config.get('distributions')
    if not distributions:
        print("No distributions specified, Aborting script.")
        return False

    for dist_key, dist_config in distributions.items():
        if dist_key == 'production':
            dir_name = mod_name
        else:
            suffix = dist_config.get('suffix')
            if suffix:
                dir_name = mod_name + suffix
            else:
                dir_name = mod_name + mod_name + " " + dist_key

        dist_config['dir_name'] = dir_name
        dist_config['path'] = os.path.join(se_mods_dir, dir_name)

        # TODO actually pull this from config
        dist_config['cleanup_ignores'] = ["^modinfo\.sbmi"]
        dist_config['cleanup_ignore_rgx'] = [
            re.compile(ignore_str) for ignore_str in dist_config['cleanup_ignores']
        ]


        compile_symbols_to_remove = dist_config.get('compile_symbols_to_remove')
        if not compile_symbols_to_remove:
            # clean this up so later code doesn't have to check for existence
            dist_config['compile_symbols_to_remove'] = None

    # tools
    mwm_builder_path = "{0}".format(config.get('mwm_builder_path'))

    return {
        'source_modules': source_modules,
        'distributions': distributions,
        'mwm_builder_path': mwm_builder_path,
    }

