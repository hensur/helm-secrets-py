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


def encrypt(file, inplace=True, outfile=sys.stdout):
    sops_args = ["-e"]
    __sops(sops_args, file, inplace, outfile)


def decrypt(file, inplace=True, outfile=sys.stdout):
    sops_args = ["-d"]
    __sops(sops_args, file, inplace, outfile)


def __sops(args, file, inplace, outfile):
    """
    args are the first sops arguments
    """
    args.insert(0, "sops")

    if inplace:
        args.extend(["-i", file])
        process = subprocess.run(args)
    else:
        args.append(file)
        process = subprocess.run(args, stdout=outfile, cwd=os.path.dirname(file))

    process.check_returncode()
