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
    load_arms_exe_path = find_path_or_throw(
        'load_arms_exe_path', loaded, install_dir,
        [se_steam_dir + '\\Bin64\\LoadARMS.exe']
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
        'load_arms_exe_path': load_arms_exe_path,
        'mwm_exe_path': mwm_exe_path,
        'se_exe_path': se_exe_path,
        'se_mods_dir': se_mods_dir,
        'se_steam_dir': se_steam_dir,
    }


def load_project_config(project_dir, plugin_build_dir, global_config):
    print('Using {}: "{}"'.format('project_dir', project_dir))
    print('Using {}: "{}"'.format('plugin_build_dir', plugin_build_dir))

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
    project_name = get(
        'project_name', loaded, str(os.path.basename(project_dir))
    )
    repo_name = get(
        'repo_name', loaded, project_name
    )
    repo_owner = get(
        'repo_owner', loaded,
        git.first_author(global_config['git_exe_path'], project_dir)
    )
    vs_version_filename = get(
        'vs_version_filename', loaded, 'VersionInfo.cs'
    )
    vs_revision_filename = get(
        'vs_revision_filename', loaded, 'VersionInfo - User.cs'
    )

    # Steam Assets
    steam_audio_dir = find_path_or_throw(
        'steam_audio_dir', loaded, project_dir,
        [project_dir + "\\Audio"]
    )
    steam_data_dir = find_path_or_throw(
        'steam_data_dir', loaded, project_dir,
        [project_dir + "\\Data"]
    )
    steam_models_dir = find_path_or_throw(
        'steam_models_dir', loaded, project_dir,
        [project_dir + "\\Models"]
    )
    steam_scripts_dir = find_path_or_throw(
        'steam_scripts_dir', loaded, project_dir,
        [project_dir + "\\Scripts\\Steam"]
    )
    steam_textures_dir = find_path_or_throw(
        'steam_textures_dir', loaded, project_dir,
        [project_dir + "\\Textures"]
    )

    # Plugin Assets
    plugin_props_dir = find_path_or_throw(
        'plugin_props_dir', loaded, project_dir,
        [project_dir + "\\Scripts\\Properties"]
    )
    plugin_build_files = get(
        'plugin_build_files', loaded,
        [project_name + '.dll']
    )

    # Return config dict
    return {
        'plugin_build_dir': plugin_build_dir,
        'plugin_build_files': plugin_build_files,
        'plugin_props_dir': plugin_props_dir,
        'project_dir': project_dir,
        'project_name': project_name,
        'repo_name': repo_name,
        'repo_owner': repo_owner,
        'steam_audio_dir': steam_audio_dir,
        'steam_data_dir': steam_data_dir,
        'steam_models_dir': steam_models_dir,
        'steam_scripts_dir': steam_scripts_dir,
        'steam_textures_dir': steam_textures_dir,
        'vs_version_filename': vs_version_filename,
        'vs_revision_filename': vs_revision_filename
    }


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
