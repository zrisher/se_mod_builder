"""
from subprocess import Popen, PIPE


def run(exe_path, json_config_path, build_dir, version, publish=False):
    command_parts = [
        exe_path, json_config_path,
        # 'version={}'.format(version), # parsing broken, now works from files
        'publish={}'.format(publish)
    ]
    print('Running SEPL command:', ' '.join(command_parts))
    proc = Popen(command_parts, stdout=PIPE, stderr=PIPE, cwd=build_dir)
    (stdout, stderr) = proc.communicate()
    if proc.returncode == 0:
        print("SEPL succeeded: {}".format(stdout.decode('ascii')))
    else:
        raise ValueError('SEPL error.\nStdout:\n{}\nStderr:\n{}'
                         .format(stdout.decode('ascii'),
                                 stderr.decode('ascii')))
"""
