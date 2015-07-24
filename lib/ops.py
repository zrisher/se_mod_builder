import os
import os.path
import re
import shutil
import fileinput
import codecs

special_chars = re.compile("[^a-zA-Z0-9_\-]")
conditional_line = re.compile("\s*\[System.Diagnostics.Conditional\(\"(.*?)\"\)\]")


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        print("creating directory path: " + dir_path)
        os.makedirs(dir_path)


def erase_dir(dir_path):
    if os.path.exists(dir_path):
        print("Removing directory path: " + dir_path)
        shutil.rmtree(dir_path)


def copy_files_with_extension(source, destination, extension,
                              filename_prefix="", comp_sym_to_remove=[]):
    """
    Copy all files with extension `extension` from `source` to `destination`.
    Optionally append `filename_prefix` to the name of the copies.
    """
    if not os.path.exists(source):
        return

    # wait to create dir until we have a file so we don't create empty dirs
    dist_dir_ensured = False

    lowercase_extension = extension.lower()
    for filename in os.listdir(source):
        if filename.lower().endswith(lowercase_extension):
            source_file_path = os.path.join(source, filename)
            if os.path.isfile(source_file_path):
                if not dist_dir_ensured:
                    create_dir(destination)
                    dist_dir_ensured = True

                dist_file_path = os.path.join(
                    destination, filename_prefix + filename
                )
                print("Copy from {0}\n       to {1}".format(
                    source_file_path, dist_file_path
                ))
                shutil.copy(source_file_path, dist_file_path)

                if lowercase_extension[-2:] == "cs":
                    preprocess_cs_file(dist_file_path, comp_sym_to_remove)


def deep_copy_files_with_extension(source, destination, extension,
                                   filename_prefix="",
                                   comp_sym_to_remove=[],
                                   squash_dirs=False):
    """
    Copy all files with extension `extension` from every folder in `source` to
    a corresponding folder in `destination`.

    Optionally append `filename_prefix` to the name of the copies.

    Optionally discard folder structure in destination and instead prefix the
    file names with their folder names in "Path.To.File.Filename" format.

    The provided filename prefix is added before the directory prefix.
    """

    for dir_path, sub_dirs, files in os.walk(source):
        rel_dir_path = os.path.relpath(dir_path, source)
        if squash_dirs:
            dist_path = destination
            squashed_dirs_file_prefix = re.sub(special_chars, '.', rel_dir_path)
            if squashed_dirs_file_prefix == ".":
                squashed_dirs_file_prefix = ''
            else:
                squashed_dirs_file_prefix += '.'

            current_file_prefix = filename_prefix + squashed_dirs_file_prefix
        else:
            dist_path = os.path.join(destination, rel_dir_path)
            current_file_prefix = filename_prefix

        copy_files_with_extension(
            dir_path, dist_path, extension, current_file_prefix,
            comp_sym_to_remove
        )



def recursive_delete_if_empty(path):
    """
    Recursively delete empty directories; return True
    if everything was deleted.
    http://stackoverflow.com/questions/26774892/how-to-find-recursively-empty-directories-in-python
    """

    if not os.path.isdir(path):
        # If you also want to delete some files like desktop.ini, check
        # for that here, and return True if you delete them.
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


def preprocess_cs_file(file_path, comp_sym_to_remove):
    """
    SE doesn't actually allow preprocessor symbol definitions in files,
    but it will remove conditional lines without defined symbols all the same

    we fake it by:
    parsing the symbol definitions, filtering for the valid ones for this distro
    removing all the symbol definition lines (so it will compile)
    removing the "System.Diagnostics.Conditional"s targeted at valid symbols
    """

    # find valid compilation symbols

    #print("Preproccess CS file {0}".format(file_path))

    encoding = get_encoding(file_path)
    valid_syms = []

    with open(file_path, 'r', encoding=encoding) as file:
        for line in file:
            if not line.startswith('#'):
                break
            if line.startswith('#define'):
                words = line.split()
                if words.__len__() > 1:
                    comp_sym = words[1]
                    if comp_sym and not \
                        (comp_sym_to_remove and comp_sym in comp_sym_to_remove):
                            valid_syms.append(comp_sym)

    # remove conditional lines for valid symbols

    print("Preproccess CS file - valid_syms: {0}".format(valid_syms))

    # note that printing within a fileinput loop actually writes to the file
    with fileinput.input(file_path, inplace=True) as file:
        for line in file:
            # remove comp definitions at top, they'll crash SE compilation
            # note we can't just check line.startswith('#define') due to encoding
            words = line.split()
            if words.__len__() > 0 and '#define' in words[0]:
                print("// Compilation Symbol Def removed by SEModHelper")
                continue

            # remove conditional lines for valid syms
            conditional_attr_line = re.match(conditional_line, line)
            if conditional_attr_line:
                conditional_on = conditional_attr_line.group(1)
                if conditional_on in valid_syms:
                    print("// Valid Symbol Conditional removed by SEModHelper")
                    continue

            # TODO check for #if #else #end conditions too

            print(line, end="")





def get_encoding(file_path):
    """
    Courtesy of http://stackoverflow.com/questions/13590749/reading-unicode-file-data-with-bom-chars-in-python
    """
    bytes = min(32, os.path.getsize(file_path))
    raw = open(file_path, 'rb').read(bytes)

    if raw.startswith(codecs.BOM_UTF8):
        encoding = 'utf-8-sig'
    else:
        result = codecs.chardet.detect(raw)
        encoding = result['encoding']

    return encoding


"""
# copied from http://stackoverflow.com/questions/1213706/what-user-do-python-scripts-run-as-in-windows/1214935#1214935
def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise

shutil.rmtree('Archive', ignore_errors=False, onerror=handleRemoveReadonly)
"""