"""
Calls sops to encrypt or decrypt a file
"""

import subprocess
import yaml
import sys


def is_enc(file):
    with open(file, "r") as f:
        doc = yaml.load(f)
        try:
            doc["sops"]["version"]
        except KeyError:
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
    sops_args = args

    if inplace:
        sops_args.extend(["-i", file])
        process = subprocess.run(sops_args)
    else:
        sops_args.append(file)
        process = subprocess.run(sops_args, stdout=outfile)

    process.check_returncode()
