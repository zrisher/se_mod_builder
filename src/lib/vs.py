import re


def set_revision_in_version_info(revision, version_path, revision_path):
    pattern = re.compile(
        '(\[assembly: AssemblyVersion\("\d*\.\d*\.\d*\.)(\d*)("\)\])'
    )
    with open(version_path, 'r') as file:
        with open(revision_path, 'w') as user_file:
            print('Writing revision "{}" to "{}"'
                  .format(revision, revision_path))
            for line in file:
                match = pattern.match(line)
                if match:
                    line = match.group(1) + str(revision) + match.group(3)
                user_file.write(line)


def get_version(version_path):
    pattern = re.compile(
        '\[assembly: AssemblyVersion\("(\d*\.\d*\.\d*\.\d*)"\)\]'
    )
    with open(version_path) as file:
        for line in file:
            match = pattern.match(line)
            if match:
                return match.group(1)


"""
return {
    "Build": match.group(1),
    "Major": match.group(2),
    "Minor": match.group(3),
    "Revision": match.group(4)
}
"""