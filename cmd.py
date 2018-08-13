import os

def deploy(dir, parent_dir):
    

def __subdir_filelist(dir, list):
    """
    Build a file list of values.yaml and secrets.yaml files
    recursively going up from a leaf directory
    """

    __subdir_file_tolist("values.yaml", dir, list)
    __subdir_file_tolist("secrets.yaml", dir, list)

    if __parent_dir(dir) is not dir:
        return __subdir_filelist(__parent_dir(dir), list)

    return list


def __parent_dir(dir):
    return os.path.abspath(os.path.join(dir, os.pardir))


def __subdir_file_tolist(file, dir, list):
    f = os.path.join(dir, file)
    if os.path.isfile(f):
        list.append(f)
