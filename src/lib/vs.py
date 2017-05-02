import re


def set_revision_in_version_info(revision, props_dir):
    pattern = re.compile(
        '(\[assembly: AssemblyVersion\("\d*\.\d*\.\d*\.)(\d*)("\)\])'
    )
    with open(props_dir + '\\VersionInfo.cs', 'r') as file:
        user_file_path = props_dir + '\\VersionInfo - User.cs'
        with open(user_file_path, 'w') as user_file:
            print('Writing revision "{}" to "{}"'
                  .format(revision, user_file_path))
            for line in file:
                match = pattern.match(line)
                if match:
                    line = match.group(1) + str(revision) + match.group(3)
                user_file.write(line)
