#!/usr/bin/env python3
"""
helm plugin to manage secret values using mozilla sops
"""

import argparse
import sys
import cmd

usage_main = """GnuPG secrets encryption in Helm Charts
This plugin provides ability to encrypt/decrypt secrets files
to store in less secure places, before they are installed using
Helm.
To decrypt/encrypt/edit you need to initialize/first encrypt secrets with
sops - https://github.com/mozilla/sops
"""


def enc_cmd(args, unknown):
    cmd.enc(args.file)


def dec_cmd(args, unknown):
    f = cmd.dec(args.file)
    print("decrypted to: " + f)


def view_cmd(args, unknown):
    cmd.view(args.file)


def clean_cmd(args, unknown):
    cmd.clean(args.dir)


def deploy_cmd(args, unknown):
    reallyskip = False
    if args.dry_run and args.skip_dec:
        reallyskip = True
        print("skipping decryption")
    ret = cmd.deploy(args.dir, args.parent, args.keep, dryrun=args.dry_run,
                     skipdec=reallyskip)
    sys.exit(ret)


def install_cmd(args, unknown):
    sys.exit(cmd.install(unknown))


def cmdline_cmd(args, unknown):
    cmd.cmdline(args.dir, args.parent)


def upgrade_cmd(args, unknown):
    sys.exit(cmd.upgrade(unknown))


def main(args):
    parser = argparse.ArgumentParser(description=usage_main)
    subparsers = parser.add_subparsers(title="commands")

    enc_parser = subparsers.add_parser("enc", help="encrypt a given file")
    enc_parser.add_argument("file", help="file to encrypt")
    enc_parser.set_defaults(func=enc_cmd)

    dec_parser = subparsers.add_parser("dec", help="decrypt a given file")
    dec_parser.add_argument("file", help="file to decrypt")
    dec_parser.set_defaults(func=dec_cmd)

    view_parser = subparsers.add_parser("view",
                                        help="view a given file (decrypted)")
    view_parser.add_argument("file", help="file to view")
    view_parser.set_defaults(func=view_cmd)

    clean_parser = subparsers.add_parser("clean",
                                         help="clean a given dir (decrypted)")
    clean_parser.add_argument("dir", help="dir to clean")
    clean_parser.set_defaults(func=clean_cmd)

    deploy_parser = subparsers.add_parser("deploy", help="wrapper for helm, \
            builds the value file list based on a leaf directory",
                                          description="test")
    deploy_parser.add_argument("dir", help="dir to deploy")
    deploy_parser.add_argument("-p", "--parent", help="parent dir of the project", default=".")
    deploy_parser.add_argument("-k", "--keep", help="keep decrypted files", action="store_true")
    deploy_parser.add_argument("--skip-dec", help="don't decrypt files if in dry-run mode", action="store_true")
    deploy_parser.add_argument("--dry-run", help="execute helm in dry-run mode \
            and print computed commands", action="store_true")
    deploy_parser.set_defaults(func=deploy_cmd)

    install_parser = subparsers.add_parser("install", help="wrapper for helm \
            install that decrypts secret files before execution")
    install_parser.set_defaults(func=install_cmd)

    upgrade_parser = subparsers.add_parser("upgrade", help="wrapper for helm \
            upgrade that decrypts secret files before execution")
    upgrade_parser.set_defaults(func=upgrade_cmd)

    cmdline_parser = subparsers.add_parser("cmdline", help="prints the helm \
            cmdline that would be executed for deployments")
    cmdline_parser.set_defaults(func=cmdline_cmd)
    cmdline_parser.add_argument("dir", help="dir to deploy")
    cmdline_parser.add_argument("-p", "--parent", help="parent dir of the project", default=".")

    parsed, unknown = parser.parse_known_args(args)

    if not args:
        parser.print_help()
        sys.exit(1)

    parsed.func(parsed, unknown)


if __name__ == "__main__":
    main(sys.argv[1:])
