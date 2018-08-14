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


def dec_cmd(args, unknown):
    print(args)


def view_cmd(args, unknown):
    print(args)


def clean_cmd(args, unknown):
    print(args)


def install_cmd(args, unknown):
    print(args)
    print(unknown)


def upgrade_cmd(args, unknown):
    print(args)


def main(args):
    parser = argparse.ArgumentParser(description=usage_main)
    subparsers = parser.add_subparsers(title="subcommands")

    enc_parser = subparsers.add_parser("enc", help="encrypt a given file")
    enc_parser.add_argument("file", help="file to encrypt")
    enc_parser.set_defaults(func=enc_cmd)

    dec_parser = subparsers.add_parser("dec", help="decrypt a given file")
    dec_parser.add_argument("file", help="file to decrypt")
    dec_parser.set_defaults(func=dec_cmd)

    view_parser = subparsers.add_parser("view", help="view a given file (decrypted)")
    view_parser.add_argument("file", help="file to view")
    view_parser.set_defaults(func=view_cmd)

    clean_parser = subparsers.add_parser("clean", help="clean a given file (decrypted)")
    clean_parser.add_argument("file", help="file to clean")
    clean_parser.set_defaults(func=clean_cmd)

    install_parser = subparsers.add_parser("install", help="wrapper for helm \
            install that decrypts secret files before execution")
    install_parser.set_defaults(func=install_cmd)

    upgrade_parser = subparsers.add_parser("upgrade", help="wrapper for helm \
            upgrade that decrypts secret files before execution")
    upgrade_parser.set_defaults(func=upgrade_cmd)

    parsed, unknown = parser.parse_known_args(args)

    if len(args) < 1:
        parser.print_help()
        sys.exit(1)

    parsed.func(parsed, unknown)


if __name__ == "__main__":
    main(sys.argv[1:])

