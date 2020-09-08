#!/usr/bin/env python3
# coding: UTF-8

import argparse
import colorama
from colorama import Fore, Back, Style

from . import manifestutil
from . import util


def cmd_todebuggable(args):
    print('Decoding APK by Apktool...')
    try:
        util.decode(args.apk_path)
    except:
        return

    print('Checking AndroidManifest.xml...')
    manifest = manifestutil.ManifestUtil(args.apk_path.replace('.apk', '') + '/AndroidManifest.xml')
    manifest.check_all()

    print(Fore.CYAN + '\nSet debuggable attribute to true in AndroidManifest!')
    manifest.to_debuggable()

    print('\nBuilding APK by Apktool...')
    dir_name = args.apk_path.replace('.apk', '')
    apk_path = args.output
    if args.output is None:
        apk_path = dir_name + ".patched.apk"

    try:
        util.build(dir_name, apk_path)
    except:
        return

    print('Signing APK by apksigner...')
    try:
        util.sign(apk_path)
    except:
        return
    print(Fore.CYAN + 'Output: ' + apk_path)


def cmd_decode(args):
    print('Decoding APK by Apktool...')
    try:
        util.decode(args.apk_path)
    except:
        return

    print('Checking AndroidManifest.xml...')
    manifest = manifestutil.ManifestUtil(args.apk_path.replace('.apk', '') + '/AndroidManifest.xml')
    manifest.check_all()


def cmd_build(args):
    print('Building APK by Apktool...')
    apk_path = args.output
    if args.output is None:
        apk_path = args.dir_name + ".patched.apk"
    try:
        util.build(args.dir_name, apk_path)
    except Exception as e:
        return

    print('Signing APK by apksigner...')
    try:
        util.sign(apk_path)
    except:
        return

    print(Fore.CYAN + 'Output: ' + apk_path)


def cmd_sign(args):
    print('Signing APK by apksigner...')
    try:
        util.sign(args.apk_path)
    except:
        return
    
    print(Fore.CYAN + 'Output: ' + args.apk_path)


def cmd_info(args):
    print('Getting package name by aapt...')
    try:
        util.get_packagename(args.apk_path)
    except:
        return


def cmd_screenshot(args):
    print('Getting a screenshot from connected device...')
    try:
        file_name = util.get_screenshot()
        print(Fore.CYAN + 'Output: ' + file_name)
    except:
        return


def main():
    colorama.init(autoreset=True)
    parser = argparse.ArgumentParser(description='apk patcher')
    subparsers = parser.add_subparsers()

    parser_todebuggable = subparsers.add_parser('debuggable', aliases=['debug', 'dg'], help='')
    parser_todebuggable.add_argument('apk_path', help='')
    parser_todebuggable.add_argument('--output', '-o')
    parser_todebuggable.set_defaults(handler=cmd_todebuggable)

    parser_decompile = subparsers.add_parser('decode', aliases=['d'], help='')
    parser_decompile.add_argument('apk_path', help='')
    parser_decompile.set_defaults(handler=cmd_decode)

    parser_build = subparsers.add_parser('build', aliases=['b'], help='')
    parser_build.add_argument('dir_name', help='')
    parser_build.add_argument('--output', '-o')
    parser_build.set_defaults(handler=cmd_build)

    parser_sign = subparsers.add_parser('sign', aliases=['s'], help='')
    parser_sign.add_argument('apk_path', help='')
    parser_sign.set_defaults(handler=cmd_sign)

    parser_info = subparsers.add_parser('info', aliases=['i'], help='')
    parser_info.add_argument('apk_path', help='')
    parser_info.set_defaults(handler=cmd_info)

    parser_screenshot = subparsers.add_parser('screenshot', aliases=['ss'], help='')
    parser_screenshot.set_defaults(handler=cmd_screenshot)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
