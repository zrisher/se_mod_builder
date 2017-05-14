import os
import yaml


def load_global_config(install_dir, asset_dir, verbose=False):
    """
    sepl_exe_path = find_path_or_throw(
        'sepl_exe_path', loaded, install_dir,
        [se_steam_dir + '\\SpaceEngineersPluginLoader\\PluginManager.exe']
    )
    """

    # Search for Github for Windows git paths too
    github_path = os.getenv('LOCALAPPDATA') + "\\GitHub"
    github_exe_paths = [
        '{}{}\\cmd\\git.exe'.format(github_path, entry)
        for entry in os.listdir(github_path)
        if entry.startswith('PortableGit_')
    ] if os.path.exists(github_path) else []
    git_default_paths = [
            r'C:\Program Files\Git\bin\git.exe',
            r'C:\Program Files (x86)\Git\bin\git.exe'
    ] + github_exe_paths

    loaded = load_config(install_dir + r'\config.yml', 'global', verbose)

    config = {
        'asset_dir': find_path(
            'asset_dir', {}, '', verbose, [asset_dir]
        ),
        'git_exe_path': find_path(
            'git_exe_path', loaded, install_dir, verbose, git_default_paths
        ),
        'install_dir': find_path(
            'install_dir', {}, '', verbose, [install_dir]
        ),
        'se_mods_dir': find_path(
            'se_mods_dir', loaded, install_dir, verbose,
            [os.path.join(os.getenv('APPDATA'), "SpaceEngineers", "Mods")]
        ),
        'se_steam_dir': find_path(
            'se_steam_dir', loaded, install_dir, verbose,
            [r'C:\Program Files\Steam\SteamApps\common\SpaceEngineers',
             r'C:\Program Files (x86)\Steam\SteamApps\common\SpaceEngineers']
        ),
    }
    config['mwm_exe_path'] = find_path(
        'mwm_exe_path', loaded, install_dir, verbose,
        [config['se_steam_dir'] + '\\Tools\\MwmBuilder\\MwmBuilder.exe']
    )
    config['se_exe_path'] = find_path(
        'se_exe_path', loaded, install_dir, verbose,
        [config['se_steam_dir'] + '\\Bin64\\SpaceEngineers.exe']
    )
    return config


def load_project_config(project_dir, plugin_build_dir, verbose=False):
    loaded = load_config(project_dir + r'\build.yml', 'project', verbose)

    return {
        'project_dir': get(
            'project_dir', {}, verbose, project_dir
        ),
        'project_name': get(
            'project_name', loaded, verbose,
            str(os.path.basename(project_dir))
        ),
        'steam_audio_dir': find_path(
            'steam_audio_dir', loaded, project_dir, verbose,
            [project_dir + "\\Audio"], True
        ),
        'steam_data_dir': find_path(
            'steam_data_dir', loaded, project_dir, verbose,
            [project_dir + "\\Data"], True
        ),
        'steam_models_dir': find_path(
            'steam_models_dir', loaded, project_dir, verbose,
            [project_dir + "\\Models"], True
        ),
        'steam_scripts_dir': find_path(
            'steam_scripts_dir', loaded, project_dir, verbose,
            [project_dir + "\\Scripts\\Steam"], True
        ),
        'steam_textures_dir': find_path(
            'steam_textures_dir', loaded, project_dir, verbose,
            [project_dir + "\\Textures"], True
        ),
        'vs_props_dir': find_path(
            'vs_props_dir', loaded, project_dir, verbose,
            [project_dir + "\\Scripts\\Properties"]
        ),
        'vs_version_filename': get(
            'vs_version_filename', loaded, verbose, 'VersionInfo.cs'
        ),
        'vs_revision_filename': get(
            'vs_revision_filename', loaded, verbose, 'VersionInfo - User.cs'
        )
    }


def find_path(param, loaded_config, root,
              verbose=False, defaults=None, optional=False):
    loaded = loaded_config.get(param)
    if loaded and not os.path.isabs(loaded):
        loaded = os.path.join(root, loaded)
    paths = [loaded] + defaults or []
    for path in paths:
        if path and os.path.exists(path):
            debug('Using {}: "{}"'.format(param, path), verbose)
            return path
    if not optional:
        raise ValueError('Unable to find "{}", tried {}'.format(param, paths))


def get(param, loaded_config, verbose=False, default=None):
    result = loaded_config.get(param, default)
    debug('Using {}: "{}"'.format(param, result), verbose)
    return result


def load_config(file_path, config_type, verbose=False):
    if os.path.exists(file_path):
        debug('Loading {} config from "{}"'
              .format(config_type, file_path), verbose)
        with open(file_path, 'r') as file:
            loaded = yaml.load(file) or {}
    else:
        debug('No {} config at "{}", using defaults.'
              .format(config_type, file_path), verbose)
        loaded = {}
    return loaded


def debug(msg, verbose):
    if verbose:
        print(msg)
