#!/usr/bin/env python3
# coding: UTF-8

import argparse
import colorama
from colorama import Fore, Back, Style

from . import check_manifest
from . import apkutil


def cmd_todebuggable(args):
    print(args.apk_name)

def cmd_decode(args):
    print('Decoding APK by Apktool...')
    apkutil.decode(args.apk_name)

    print('Checking AndroidManifest.xml...')
    manifest = check_manifest.CheckManifest(args.apk_name.replace('.apk', '') + '/AndroidManifest.xml')
    colorama.init(autoreset=True)
    print('Permission:')
    print(manifest.get_permissions())
    print('Debuggable:')
    if manifest.is_debuggable():
        print(Fore.RED + 'True')
    else:
        print(Fore.BLUE + 'False')
    print('AllowBackup:')
    if manifest.is_allowBackup():
        print(Fore.RED + 'True')
    else:
        print(Fore.BLUE + 'False')

def cmd_build(args):
    print('Building APK by Apktool...')
    if args.output is None:
        apk_name = args.dir_name + ".patched.apk"

    apkutil.build(args.dir_name, apk_name)

def cmd_sign(args):
    print('Signing APK by apksigner...')
    apkutil.sign(args.apk_name)

def main():
    parser = argparse.ArgumentParser(description='apk patcher')
    subparsers = parser.add_subparsers()

    parser_todebuggable = subparsers.add_parser('debuggable', help='')
    parser_todebuggable.add_argument('apk_name', help='')
    parser_todebuggable.set_defaults(handler=cmd_todebuggable)

    parser_decompile = subparsers.add_parser('decode', aliases=['d'], help='')
    parser_decompile.add_argument('apk_name', help='')
    parser_decompile.set_defaults(handler=cmd_decode)

    parser_comple = subparsers.add_parser('build', aliases=['b'], help='')
    parser_comple.add_argument('dir_name', help='')
    parser_comple.add_argument('--output', '-o')
    parser_comple.set_defaults(handler=cmd_build)

    parser_comple = subparsers.add_parser('sign', help='')
    parser_comple.add_argument('apk_name', help='')
    parser_comple.set_defaults(handler=cmd_sign)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
