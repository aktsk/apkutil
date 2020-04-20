#!/usr/bin/env python3
# coding: UTF-8

import argparse
import colorama
from colorama import Fore, Back, Style

from . import manifestutil
from . import apkutil


def cmd_todebuggable(args):
    print('Decoding APK by Apktool...')
    apkutil.decode(args.apk_name)

    print('Checking AndroidManifest.xml...')
    manifest = manifestutil.ManifestUtil(args.apk_name.replace('.apk', '') + '/AndroidManifest.xml')
    manifest.check_all()

    colorama.init(autoreset=True)
    print(Fore.CYAN + '\nSet debuggable attribute to true in AndroidManifest!')
    manifest.to_debuggable()

    print('\nBuilding APK by Apktool...')
    dir_name = args.apk_name.replace('.apk', '')
    apk_name = args.output
    if args.output is None:
        apk_name = dir_name + ".patched.apk"
    apkutil.build(dir_name, apk_name)
    print(Fore.CYAN + 'Output: ' + apk_name)

def cmd_decode(args):
    print('Decoding APK by Apktool...')
    apkutil.decode(args.apk_name)

    print('Checking AndroidManifest.xml...')
    manifest = manifestutil.ManifestUtil(args.apk_name.replace('.apk', '') + '/AndroidManifest.xml')
    manifest.check_all()

def cmd_build(args):
    print('Building APK by Apktool...')
    apk_name = args.output
    if args.output is None:
        apk_name = args.dir_name + ".patched.apk"
    apkutil.build(args.dir_name, apk_name)
    print(Fore.CYAN + 'Output: ' + apk_name)

def cmd_sign(args):
    print('Signing APK by apksigner...')
    apkutil.sign(args.apk_name)

def main():
    parser = argparse.ArgumentParser(description='apk patcher')
    subparsers = parser.add_subparsers()

    parser_todebuggable = subparsers.add_parser('debuggable', help='')
    parser_todebuggable.add_argument('apk_name', help='')
    parser_todebuggable.add_argument('--output', '-o')
    parser_todebuggable.set_defaults(handler=cmd_todebuggable)

    parser_decompile = subparsers.add_parser('decode', aliases=['d'], help='')
    parser_decompile.add_argument('apk_name', help='')
    parser_decompile.set_defaults(handler=cmd_decode)

    parser_build = subparsers.add_parser('build', aliases=['b'], help='')
    parser_build.add_argument('dir_name', help='')
    parser_build.add_argument('--output', '-o')
    parser_build.set_defaults(handler=cmd_build)

    parser_sign = subparsers.add_parser('sign', help='')
    parser_sign.add_argument('apk_name', help='')
    parser_sign.set_defaults(handler=cmd_sign)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
