import os
import shutil
from .lib import git, mwm, ops, se, sepl, vs


def build_models(global_config, project_config):
    model_processes = mwm.start_builds('a', 'b')
    mwm.await_builds(model_processes)


def distribute_steam(global_config, project_config):
    dst = global_config['se_mods_dir'] + "\\" + project_config['project_name']
    print('Distributing steam assets to "{}".'.format(dst))
    ops.distribute(project_config['steam_audio_dir'],
                   dst + '\\Audio', '.xwm')
    ops.distribute(project_config['steam_data_dir'],
                   dst + '\\Data', '.sbc')
    ops.distribute(project_config['steam_models_dir'],
                   dst + '\\Models', '.mwm')
    ops.distribute(project_config['steam_textures_dir'],
                   dst + '\\Textures', '.dds')

    scripts_src = project_config['steam_scripts_dir']
    scripts_dst = dst + "\\Data\\Scripts\\" + os.path.basename(scripts_src)
    print('Distributing steam scripts to "{}".'.format(scripts_dst))
    ops.distribute(scripts_src, scripts_dst, '.cs', src_ignores=['bin', 'obj'])

    # clean dist dir
    ops.recursive_delete_if_empty(dst)


"""
def distribute_plugin(global_config, project_config, publish=False):
    src = project_config['plugin_build_dir']
    version = vs.get_version(
        project_config['plugin_props_dir'] + "\\" +
        project_config['vs_revision_filename']
    )
    print('Distributing plugin assets from "{}".'.format(src))
    sepl.run(
        global_config['sepl_exe_path'],
        project_config['plugin_json_path'],
        src, version, publish=publish
    )
"""


def example_global_config(asset_dir, target_dir):
    template_path = asset_dir + '\\config.example.yml'
    dst_path = target_dir + '\\config.yml'
    print('Generating global config at "{}" from template at "{}"'
          .format(dst_path, template_path))
    shutil.copy2(template_path, dst_path)


def example_project_config(asset_dir, target_dir):
    template_path = asset_dir + '\\build.example.yml'
    dst_path = target_dir + '\\build.yml'
    print('Generating project config at "{}" from template at "{}"'
          .format(dst_path, template_path))
    shutil.copy2(template_path, dst_path)


def git_version(global_config, project_config):
    git_description = git.describe(
        global_config['git_exe_path'],
        project_config['project_dir']
    )
    revision = git_description.get('revision', 0)
    if git_description.get('dirty'):
        revision += 1
    vs.set_revision_in_version_info(
        revision,
        project_config['vs_props_dir'] + '\\' +
        project_config['vs_version_filename'],
        project_config['vs_props_dir'] + '\\' +
        project_config['vs_revision_filename']
    )


def kill_se(global_config, project_config):
    se.kill_processes()
    se.await_processes_killed()


def start_se(global_config, project_config):
    se.start_process(global_config['se_exe_path'])
