import os
from subprocess import Popen, PIPE


def run(exe_path, repo_owner, repo_name, build_dir, rel_src_paths,
        version=None, publish=False):
    author_flag = "--author={}".format(repo_owner)
    repo_flag = "--repo={}".format(repo_name)
    command = [exe_path, author_flag, repo_flag]
    if publish:
        command.append('--publish')
    if version:
        command.append('--version={}'.format(version))
    command += rel_src_paths

    print('Running Load-ARMS command:', ' '.join(command))
    proc = Popen(command, stdout=PIPE, stderr=PIPE, cwd=build_dir)
    (stdout, stderr) = proc.communicate()
    if proc.returncode == 0:
        print("Load-ARMS succeeded: {}".format(stdout.decode('ascii')))
    else:
        raise ValueError('Load-ARMS error.\nStdout:\n{}\nStderr:\n{}'
                         .format(stdout.decode('ascii'),
                                 stderr.decode('ascii')))
