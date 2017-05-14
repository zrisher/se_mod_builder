import os
import shutil


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        print('Creating directory "{}"'.format(dir_path))
        os.makedirs(dir_path)


def erase_dir(dir_path):
    if os.path.exists(dir_path):
        print('Removing directory "{}"'.format(dir_path))
        shutil.rmtree(dir_path)


def distribute(src, dst, ext, src_ignores=[], dst_ignores=[]):
    """
    Remove everything in dst unless it's up-to-date with a src file.
    Copy all files with `ext` from `src` to `dst` besides already up-to-date.
    Copies recursively and respects folder structure.
    """
    # normalize all paths for comparison
    src = os.path.realpath(src)
    dst = os.path.realpath(dst)
    ext = ext.lower()
    src_ignores = [os.path.realpath(os.path.join(src, x)) for x in src_ignores]
    dst_ignores = [os.path.realpath(os.path.join(dst, x)) for x in dst_ignores]

    # Remove all files in dst besides those that are up-to-date already
    for dir_path, dir_names, file_names in os.walk(dst):
        for file_name in file_names:
            if file_name.lower().endswith(ext):
                dst_file_path = os.path.join(dir_path, file_name)
                src_file_path = dst_file_path.replace(dst, src)
                if any(ignore in dst_file_path for ignore in dst_ignores):
                    # print('Ignoring dst file "{}"'.format(dst_file_path))
                    continue
                if not os.path.isfile(src_file_path):
                    print('Deleting orphan file "{}"'.format(dst_file_path))
                    os.remove(dst_file_path)
                elif os.path.getmtime(dst_file_path) != \
                        os.path.getmtime(src_file_path):
                    # print('Deleting updated file "{}"'.format(dst_file_path))
                    os.remove(dst_file_path)

    # Copy all files in src that don't exist in dst
    for dir_path, dir_names, file_names in os.walk(src):
        for file_name in file_names:
            if file_name.lower().endswith(ext):
                src_file_path = os.path.join(dir_path, file_name)
                dst_dir_path = dir_path.replace(src, dst)
                dst_file_path = src_file_path.replace(src, dst)
                if any(ignore in src_file_path for ignore in src_ignores):
                    # print('Ignoring src file "{}"'.format(src_file_path))
                    continue
                if os.path.exists(dst_file_path):
                    # print('Skipping exists "{}"'.format(dst_file_path))
                    continue
                if not os.path.isdir(dst_dir_path):
                    create_dir(dst_dir_path)
                print('Copy "{}" to "{}"'.format(src_file_path, dst_file_path))
                shutil.copy2(src_file_path, dst_file_path)


def recursive_delete_if_empty(path):
    """
    Recursively delete empty directories
    Return True if everything was deleted.
    http://stackoverflow.com/questions/26774892/how-to-find-recursively-empty-directories-in-python
    """
    if not os.path.isdir(path):
        return False

    # Note that the list comprehension here is necessary, a
    # generator expression would shortcut and we don't want that!
    if all([recursive_delete_if_empty(os.path.join(path, filename))
            for filename in os.listdir(path)]):
        # Either there was nothing here or it was all deleted
        os.rmdir(path)
        return True
    else:
        return False
