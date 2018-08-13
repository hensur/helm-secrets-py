#!/usr/bin/env python3
"""
helm plugin to manage secret values using mozilla sops
"""

import argparse
import sys

usage_main = """GnuPG secrets encryption in Helm Charts
This plugin provides ability to encrypt/decrypt secrets files
to store in less secure places, before they are installed using
Helm.
To decrypt/encrypt/edit you need to initialize/first encrypt secrets with
sops - https://github.com/mozilla/sops
"""


def enc_cmd(args, unknown):
    print("hello")
    print(args)


def install_cmd(args, unknown):
    print(args)
    print(unknown)


def main(args):
    parser = argparse.ArgumentParser(description=usage_main)
    subparsers = parser.add_subparsers(title="subcommands")

    enc_parser = subparsers.add_parser("enc", help="encrypt a given file")
    enc_parser.add_argument("file", help="file to encrypt")
    enc_parser.set_defaults(func=enc_cmd)

    dec_parser = subparsers.add_parser("dec", help="decrypt a given file")
    dec_parser.add_argument("file", help="file to decrypt")

    install_parser = subparsers.add_parser("install", help="wrapper for helm \
            install that decrypts secret files before execution")
    install_parser.set_defaults(func=install_cmd)

    parsed, unknown = parser.parse_known_args(args)
    parsed.func(parsed, unknown)

    if len(args) < 1:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])

