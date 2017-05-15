import os
import yaml
from .logging import log
from .git import github_windows_exe_paths


def load_global_config(install_dir):
    loaded = load_config(install_dir + r'\config.yml', 'global')

    config = {
        'git_exe_path': find_path(
            'git_exe_path', loaded, install_dir,
            github_windows_exe_paths() +
            [r'C:\Program Files\Git\bin\git.exe',
             r'C:\Program Files (x86)\Git\bin\git.exe']
        ),
        'install_dir': find_path(
            'install_dir', {}, '', [install_dir]
        ),
        'se_mods_dir': find_path(
            'se_mods_dir', loaded, install_dir,
            [os.path.join(os.getenv('APPDATA'), "SpaceEngineers", "Mods")]
        ),
        'se_steam_dir': find_path(
            'se_steam_dir', loaded, install_dir,
            [r'C:\Program Files\Steam\SteamApps\common\SpaceEngineers',
             r'C:\Program Files (x86)\Steam\SteamApps\common\SpaceEngineers']
        ),
    }
    config['mwm_exe_path'] = find_path(
        'mwm_exe_path', loaded, install_dir,
        [config['se_steam_dir'] + '\\Tools\\MwmBuilder\\MwmBuilder.exe']
    )
    config['se_exe_path'] = find_path(
        'se_exe_path', loaded, install_dir,
        [config['se_steam_dir'] + '\\Bin64\\SpaceEngineers.exe']
    )
    return config


def load_project_config(project_dir):
    loaded = load_config(project_dir + r'\build.yml', 'project')

    return {
        'project_dir': get(
            'project_dir', {}, project_dir
        ),
        'project_name': get(
            'project_name', loaded,
            str(os.path.basename(project_dir))
        ),
        'steam_audio_dir': find_path(
            'steam_audio_dir', loaded, project_dir,
            [project_dir + "\\Audio"], True
        ),
        'steam_data_dir': find_path(
            'steam_data_dir', loaded, project_dir,
            [project_dir + "\\Data"], True
        ),
        'steam_models_dir': find_path(
            'steam_models_dir', loaded, project_dir,
            [project_dir + "\\Models"], True
        ),
        'steam_scripts_dir': find_path(
            'steam_scripts_dir', loaded, project_dir,
            [project_dir + "\\Scripts\\Steam"], True
        ),
        'steam_textures_dir': find_path(
            'steam_textures_dir', loaded, project_dir,
            [project_dir + "\\Textures"], True
        ),
        'vs_props_dir': find_path(
            'vs_props_dir', loaded, project_dir,
            [project_dir + "\\Scripts\\Properties"]
        ),
        'vs_version_filename': get(
            'vs_version_filename', loaded, 'VersionInfo.cs'
        ),
        'vs_revision_filename': get(
            'vs_revision_filename', loaded, 'VersionInfo - User.cs'
        )
    }


def find_path(param, loaded_config, root, defaults=None, optional=False):
    loaded = loaded_config.get(param)
    if loaded and not os.path.isabs(loaded):
        loaded = os.path.join(root, loaded)
    paths = [loaded] + defaults or []
    for path in paths:
        if path and os.path.exists(path):
            log('Using {}: "{}"'.format(param, path))
            return path
    if not optional:
        raise ValueError('Unable to find "{}", tried {}'.format(param, paths))


def get(param, loaded_config, default=None):
    result = loaded_config.get(param, default)
    log('Using {}: "{}"'.format(param, result))
    return result


def load_config(file_path, config_type):
    if os.path.exists(file_path):
        log('Loading {} config from "{}"'.format(config_type, file_path))
        with open(file_path, 'r') as file:
            loaded = yaml.load(file) or {}
        return loaded
    else:
        log('No {} config at "{}". Defaulting.'.format(config_type, file_path))
        return {}
