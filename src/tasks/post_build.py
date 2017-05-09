import os
from ..lib import ops, load_arms, se, mwm, vs


def post_build(global_config, project_config, env):
    model_processes = mwm.start_builds('a', 'b')
    se.kill_processes()
    mwm.await_builds(model_processes)
    distribute_steam(global_config, project_config)
    se.await_processes_killed()
    distribute_load_arms(global_config, project_config,
                         publish=(env == 'release'))
    if env != 'release':
        se.start_process(global_config['se_exe_path'])


def distribute_steam(global_config, project_config):
    """
    """
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


def distribute_load_arms(global_config, project_config, publish=False):
    src = project_config['plugin_build_dir']
    version = vs.get_version(
        project_config['plugin_props_dir'] + "\\" +
        project_config['vs_revision_filename']
    )
    print('Distributing load-arms assets from "{}".'.format(src))
    load_arms.run(
        global_config['load_arms_exe_path'],
        project_config['repo_owner'],
        project_config['repo_name'],
        src,
        project_config['plugin_build_files'],
        version=version,
        publish=publish
    )
