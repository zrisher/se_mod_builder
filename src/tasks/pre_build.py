from ..lib import git
from ..lib import vs


def pre_build(global_config, project_config):
    git_description = git.describe(
        global_config['git_exe_path'],
        project_config['project_dir']
    )
    revision = git_description.get('revision', 0)
    if git_description.get('dirty'):
        revision += 1
    vs.set_revision_in_version_info(
        revision,
        project_config['plugin_props_dir'] + '\\' +
        project_config['vs_version_filename'],
        project_config['plugin_props_dir'] + '\\' +
        project_config['vs_revision_filename']
    )
