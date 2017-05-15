"""
from subprocess import Popen, PIPE


def run_sepl(exe_path, json_config_path, build_dir, publish=False):
    command_parts = [exe_path, json_config_path, 'publish={}'.format(publish)]
    print('Running SEPL command:', ' '.join(command_parts))
    proc = Popen(command_parts, stdout=PIPE, stderr=PIPE, cwd=build_dir)
    (stdout, stderr) = proc.communicate()
    if proc.returncode == 0:
        print("SEPL succeeded: " + stdout.decode('ascii'))
    else:
        raise ValueError('SEPL error.\nStdout:\n{}\nStderr:\n{}'
                         .format(stdout.decode('ascii'),
                                 stderr.decode('ascii')))
"""
