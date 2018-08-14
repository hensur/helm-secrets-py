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


def __helm_wrapper(mode, args):
    secrets_regex = re.compile(r"^(.*\/)?secrets(\.dec)?\.yaml$")
    dec_files = []
    cmd_args = ["helm", mode]

    for f in args:
        if secrets_regex.match(f):
            # We found a file, decrypt it
            dec(f)
            dec_files.append(f)
        cmd_args.append(f)

    subprocess.run(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for f in dec_files:
        enc(f, remove=True)


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
