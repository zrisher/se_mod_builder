import os
import yaml
from . import git


def load_global_config(install_dir, asset_dir):
    # Load config file
    file_path = install_dir + r'\config.yml'
    if os.path.exists(file_path):
        print('Loading global config from "{}"'.format(file_path))
        loaded = yaml.load(open(file_path, 'r')) or {}
    else:
        print('No global config file at "{}", assuming defaults.'
              .format(file_path))
        loaded = {}

    # Discover & validate params
    github_path = os.getenv('LOCALAPPDATA') + "\\GitHub"
    github_exe_paths = [
        '{}{}\\cmd\\git.exe'.format(github_path, entry)
        for entry in os.listdir(github_path)
        if entry.startswith('PortableGit_')
    ] if os.path.exists(github_path) else []
    git_exe_path = find_path_or_throw(
        'git_exe_path', loaded, install_dir, [
            r'C:\Program Files\Git\bin\git.exe',
            r'C:\Program Files (x86)\Git\bin\git.exe'
        ] + github_exe_paths
    )
    se_mods_dir = find_path_or_throw(
        'se_mods_dir', loaded, install_dir,
        [os.path.join(os.getenv('APPDATA'), "SpaceEngineers", "Mods")]
    )
    se_steam_dir = find_path_or_throw(
        'se_steam_dir', loaded, install_dir,
        [r'C:\Program Files\Steam\SteamApps\common\SpaceEngineers',
         r'C:\Program Files (x86)\Steam\SteamApps\common\SpaceEngineers']
    )
    sepl_exe_path = find_path_or_throw(
        'sepl_exe_path', loaded, install_dir,
        [se_steam_dir + '\\SpaceEngineersPluginLoader\\PluginManager.exe']
    )
    mwm_exe_path = find_path_or_throw(
        'mwm_exe_path', loaded, install_dir,
        [se_steam_dir + '\\Tools\\MwmBuilder\\MwmBuilder.exe']
    )
    se_exe_path = find_path_or_throw(
        'se_exe_path', loaded, install_dir,
        [se_steam_dir + '\\Bin64\\SpaceEngineers.exe']
    )

    # Return config dict
    return {
        'asset_dir': asset_dir,
        'git_exe_path': git_exe_path,
        'install_dir': install_dir,
        'mwm_exe_path': mwm_exe_path,
        'se_exe_path': se_exe_path,
        'se_mods_dir': se_mods_dir,
        'se_steam_dir': se_steam_dir,
        'sepl_exe_path': sepl_exe_path,
    }


def load_project_config(project_dir, plugin_build_dir):
    print('Using project_dir: "{}"'.format(project_dir))
    print('Using plugin_build_dir: "{}"'.format(plugin_build_dir))
    config = {
        'plugin_build_dir': plugin_build_dir,
        'project_dir': project_dir,
    }

    # Load config file
    file_path = project_dir + r'\build.yml'
    if os.path.exists(file_path):
        print('Loading project config from "{}"'.format(file_path))
        loaded = yaml.load(open(file_path, 'r')) or {}
    else:
        print('No project config file at "{}", assuming defaults.'
              .format(file_path))
        loaded = {}

    # Project properties
    config['project_name'] = get(
        'project_name', loaded, str(os.path.basename(project_dir))
    )

    # Plugin Assets
    config['build_plugin'] = get('build_plugin', loaded, True)
    if config['build_plugin']:
        config['plugin_props_dir'] = find_path_or_throw(
            'plugin_props_dir', loaded, project_dir,
            [project_dir + "\\Scripts\\Properties"]
        )
        config['plugin_json_path'] = find_path_or_throw(
            'plugin_json_path', loaded, project_dir,
            [project_dir + "\\plugin.json"]
        )
        config['vs_version_filename'] = get(
            'vs_version_filename', loaded, 'VersionInfo.cs'
        )
        config['vs_revision_filename'] = get(
            'vs_revision_filename', loaded, 'VersionInfo - User.cs'
        )

    # Steam Assets
    config['build_steam'] = get('build_steam', loaded, True)
    if config['build_steam']:
        config['steam_audio_dir'] = find_path_or_throw(
            'steam_audio_dir', loaded, project_dir,
            [project_dir + "\\Audio"]
        )
        config['steam_data_dir'] = find_path_or_throw(
            'steam_data_dir', loaded, project_dir,
            [project_dir + "\\Data"]
        )
        config['steam_models_dir'] = find_path_or_throw(
            'steam_models_dir', loaded, project_dir,
            [project_dir + "\\Models"]
        )
        config['steam_scripts_dir'] = find_path_or_throw(
            'steam_scripts_dir', loaded, project_dir,
            [project_dir + "\\Scripts\\Steam"]
        )
        config['steam_textures_dir'] = find_path_or_throw(
            'steam_textures_dir', loaded, project_dir,
            [project_dir + "\\Textures"]
        )

    # Return config dict
    return config


def find_path_or_throw(param, loaded_config, root, defaults):
    loaded = loaded_config.get(param)
    if loaded and not os.path.isabs(loaded):
        loaded = os.path.join(root, loaded)
    paths = [loaded] + defaults
    for path in paths:
        if path and os.path.exists(path):
            print('Using {}: "{}"'.format(param, path))
            return path
    raise ValueError('Unable to find "{}", tried {}'.format(param, paths))


def get(param, loaded_config, default):
    result = loaded_config.get(param, default)
    print('Using {}: "{}"'.format(param, result))
    return result
