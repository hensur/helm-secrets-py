"""
Handle helm secret encryption cmd
"""

import sops
import os
import shutil
import sys
import glob
import re
import subprocess
from pathlib import Path


def enc(file, remove=False):
    """
    Encrypts the given file in its directory

    If the file is already encrypted, a corresponding secrets.dec.yaml
    will be encrypted to the original file location.
    """

    if sops.is_enc(file):
        if os.path.isfile(__decfile(file)) \
                and not sops.is_enc(__decfile(file)):
            # we can encrypt the .dec.yaml file
            with open(file, "w") as of:
                sops.encrypt(__decfile(file), inplace=False, outfile=of)
                if remove:
                    os.remove(__decfile(file))
        else:
            raise FileExistsError("file is already encrypted")
    else:
        if __is_decfile(file):
            file = __encfile(file)
        sops.encrypt(file)


def dec(file):
    """
    Decrypt file to .dec.yaml file
    """

    if not sops.is_enc(file):
        raise FileExistsError("file is not encrypted")

    with open(__decfile(file), "w") as of:
        sops.decrypt(file, inplace=False, outfile=of)

    return __decfile(file)


def view(file):
    """
    Display a file to stdout
    """

    if sops.is_enc(file):
        sops.decrypt(file, inplace=False)
    else:
        with open(file, "r") as f:
            shutil.copyfileobj(f, sys.stdout)


def clean(dir):
    """
    encrypt and remove all secrets.dec.yaml files in workdir
    """
    for f in glob.iglob(os.path.join(dir, '/**/*.dec.yaml'), recursive=True):
        enc(f, remove=True)


def install(args):
    """
    helm install wrapper that decrypts all files, calls helm and
    encrypts the files again
    """
    __helm_wrapper("install", args)


def upgrade(args):
    """
    same as install
    """
    __helm_wrapper("upgrade", args)


def __helm_wrapper(mode, args, keep=False):
    secrets_regex = re.compile(r"^(.*\/)?secrets(\.dec)?\.yaml$")
    dec_files = []
    cmd_args = ["helm", mode]

    for idx, f in enumerate(args):
        arg = f
        if secrets_regex.match(f):
            # We found a file, decrypt it
            try:
                arg = dec(f)
            except FileExistsError:
                print("file was not encrypted")
            dec_files.append(f)
        cmd_args.append(arg)

    print("helm cmd:")
    print(' '.join(cmd_args))
    # subprocess.run(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if not keep:
        for f in dec_files:
            enc(f, remove=True)
    else:
        print("these files have been kept decrypted:")
        print(' '.join(dec_files))
        print("encrypt them with ./secrets.py enc")


def __decfile(infile):
    if not __is_decfile(infile):
        return os.path.splitext(infile)[0] + ".dec.yaml"
    else:
        return infile


def __encfile(infile):
    if __is_decfile(infile):
        # strips 2 times: .dec.yaml and appends .yaml
        return os.path.splitext(os.path.splitext(infile)[0]) + ".yaml"
    else:
        return infile


def __is_decfile(infile):
    return infile.endswith(".dec.yaml")


def deploy(mode, dir, parent_dir, keep):
    """
    Collect all values and secrets from a leaf directory
    and execute helm install or upgrade
    """
    dir = Path(dir).resolve()
    parent_dir = Path(parent_dir).resolve()

    if not re.match(r'(upgrade|install)', mode):
        raise ValueError("mode not supported")

    if not dir.is_dir():
        raise NotADirectoryError("{} does not exist".format(dir))

    if len([name for name in dir.iterdir()
            if os.path.isdir(os.path.join(dir, name))]) > 0:
        raise ValueError("{} has subdirectories".format(dir))

    if (Path(os.path.commonpath([dir, parent_dir])) != parent_dir):
        raise ValueError("{} is not a leaf in {}".format(dir, parent_dir))

    helm_cmd = []
    [helm_cmd.extend(["-f", f])
        for f in __subdir_filelist(dir, parent_dir, [])]

    if mode == "install":
        helm_cmd.append("-n")

    pName = dir.relative_to(parent_dir).parts[0]  # project name
    helm_cmd.append(pName)
    helm_cmd.append(str(parent_dir/pName))

    __helm_wrapper(mode, helm_cmd, keep=keep)


def __subdir_filelist(dir, parent_dir, list):
    """
    Build a file list of values.yaml and secrets.yaml files
    recursively going up from a leaf directory
    """

    __subdir_file_tolist("values.yaml", dir, list)
    __subdir_file_tolist("secrets.yaml", dir, list)

    if parent_dir == dir:
        return list

    return __subdir_filelist(dir.parent, parent_dir, list)


def __subdir_file_tolist(file, dir, list):
    f = os.path.join(dir, file)
    if os.path.isfile(f):
        list.append(f)
