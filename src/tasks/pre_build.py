from ..lib import git
from ..lib import vs


def pre_build(global_config, project_config):
    git_description = git.describe(global_config['git_exe_path'],
                                   project_config['project_dir'])
    revision = git_description.get('revision', 0)
    revision = revision + 1 if git_description.get('dirty') else revision
    props_dir = project_config['properties_dir']
    vs.set_revision_in_version_info(revision, props_dir)
