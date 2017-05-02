import re
from subprocess import Popen, PIPE


"""
def git_version_at_path(exe_path):
    \"""
    Returns the version of git installed at exe_path or None on failure
    \"""
    proc = Popen([exe_path, "--version"], stdout=PIPE, stderr=PIPE)
    (stdout, stderr) = proc.communicate()
    if proc.returncode == 0:
        return re.findall(r'\d.*$', stdout.decode('ascii'))[0]
    else:
        raise ValueError('Git error: {}'.format(stderr.decode('ascii')))
"""


def first_commit(exe_path, repo_path):
    proc = Popen([exe_path, "rev-list", "--max-parents=0", "HEAD"],
                 stdout=PIPE, stderr=PIPE, cwd=repo_path)
    (stdout, stderr) = proc.communicate()
    if proc.returncode == 0:
        return stdout.decode('ascii').strip()
    else:
        raise ValueError('Git error: {}'.format(stderr.decode('ascii')))


def first_author(exe_path, repo_path):
    commit = first_commit(exe_path, repo_path)
    command = [exe_path, "show", "-s", "--format='%an'", commit]
    proc = Popen(command, stdout=PIPE, stderr=PIPE, cwd=repo_path)
    (stdout, stderr) = proc.communicate()
    if proc.returncode == 0:
        return stdout.decode('ascii')[1:-2]
    else:
        raise ValueError('Git error: {}'.format(stderr.decode('ascii')))


def describe(exe_path, repo_path):
    proc = Popen([exe_path, "describe", "--always", "--dirty", "--tags"],
                 stdout=PIPE, stderr=PIPE, cwd=repo_path)
    (stdout, stderr) = proc.communicate()
    if proc.returncode == 0:
        return parse_describe_output(stdout.decode('ascii'))
    else:
        raise ValueError('Git error: {}'.format(stderr.decode('ascii')))


def parse_describe_output(out):
    out = out.strip()

    # Sometime it ends with -dirty
    dirty = out.endswith('-dirty')
    out = out[0:-6] if dirty else out

    # Sometimes it's just a commit
    commit_only_match = re.compile('^([a-z0-9]{7})$').match(out)
    if commit_only_match:
        return {
            'commit': commit_only_match.group(1),
            'dirty': dirty,
        }

    # Sometimes its tag-revision-commit
    tag_rev_commit_match = re.compile('^(.*)-(\d)-([a-z0-9]{8})$').match(out)
    if tag_rev_commit_match:
        return {
            'commit': tag_rev_commit_match.group(3),
            'dirty': dirty,
            'revision': int(tag_rev_commit_match.group(2)),
            'tag': tag_rev_commit_match.group(1),
        }

    # Otherwise it's just a tag
    return {
        'dirty': dirty,
        'tag': out,
    }
