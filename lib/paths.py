import os
import os.path
import re


def modules(source_dir):
    """
    Get the paths to each included module, return a dictionary mapping
    module_name: module_path
    """
    excluded_dirs = re.compile("[\.|_]")
    modules = {}

    for directory in os.listdir(source_dir):
        directory_path = os.path.join(source_dir, directory)
        if os.path.isdir(directory_path) and not re.match(excluded_dirs, directory):
            modules[directory] = directory_path

    return modules


def investigate_bad_path(s_printName, s_path):
    if s_path is os.devnull:
      print (s_printName + " set to null device")
    else:
      print ("ERROR: incorrect path to " + s_printName)
      lastPath = s_path
      while (not os.path.exists(s_path)):
        if (len(s_path) == 0):
          break
        if (s_path[-1] is "\\"):
          s_path = s_path[:-1]
        lastPath = s_path
        s_path = os.path.dirname(s_path)
      print ("\tbad path:  " + lastPath)
      print ("\tgood path: " + s_path)


def find_file_up(file_name, dir_path, max_levels=5):
    """
    Return the path to the first file named `file_name`
    Look in `start_dir`, then `max_levels` dirs above until it's found
    """
    level = 1
    while (level <= max_levels):
        file_path = os.path.join(dir_path, file_name)
        if os.path.exists(file_path):
            return file_path;
        else:
            dir_path = os.path.dirname(dir_path)
            level += 1

    return False






