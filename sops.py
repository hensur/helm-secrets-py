"""
Calls sops to encrypt or decrypt a file
"""

import subprocess
import yaml
import sys
import os


def is_enc(file):
    with open(file, "r") as f:
        doc = yaml.load(f)
        try:
            doc["sops"]["version"]
        except (KeyError, TypeError):
            return False
    return True


def encrypt(infile, inplace=True, outfile=sys.stdout):
    sops_args = ["-e"]
    __sops(sops_args, infile, inplace, outfile)


def decrypt(infile, inplace=True, outfile=sys.stdout):
    sops_args = ["-d"]
    __sops(sops_args, infile, inplace, outfile)


def __sops(args, infile, inplace, outfile):
    """
    args are the first sops arguments
    """
    args.insert(0, "sops")

    f = os.path.basename(infile)
    wd = os.path.dirname(infile)
    if not wd:
        wd = os.getcwd()
    if inplace:
        args.extend(["-i", f])
        process = subprocess.run(args, cwd=wd)
    else:
        args.append(f)
        process = subprocess.run(args, stdout=outfile, cwd=wd)

    process.check_returncode()
