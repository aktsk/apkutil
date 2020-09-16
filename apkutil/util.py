#!/usr/bin/env python3
# coding: UTF-8

import datetime
import glob
import json
import os
import subprocess
from colorama import Fore


def decode(apk_path):
    apktool_cmd = ['apktool']
    apktool_cmd.extend(['d', apk_path])

    try:
        proc = subprocess.Popen(apktool_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        outs, errs = proc.communicate()
        if (outs is not None) and (len(outs) != 0):
            print(outs.decode('ascii'))
        
        if (errs is not None) and (len(errs) != 0):
            errs = errs.decode('ascii')
            # unsupported `apktool d -f`
            errs = errs.replace('Use -f switch if you want to overwrite it.', '')
            raise Exception(errs)

    except FileNotFoundError as e:
        print('apktool not found.')
        print('Please install apktool')


def build(dir_name, apk_path):
    apktool_cmd = ['apktool']
    apktool_cmd.extend(['b', dir_name])
    apktool_cmd.extend(['-o', apk_path])
    try:
        proc = subprocess.Popen(apktool_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        outs, errs = proc.communicate()
        if (outs is not None) and (len(outs) != 0):
            print(outs.decode('ascii'))
        
        if (errs is not None) and (len(errs) != 0):
            errs = errs.decode('ascii')
            raise Exception(errs)

    except FileNotFoundError as e:
        print('apktool not found.')
        print('Please install apktool.')


def sign(apk_path):
    home_dir = os.environ['HOME']
    keystore_path = ''
    ks_key_alias = ''
    ks_pass = ''

    try:
        with open(home_dir + "/apkutil.json") as f:
            config = json.load(f)
            keystore_path = config['keystore_path'].replace('~', home_dir)
            ks_key_alias = config['ks-key-alias']
            ks_pass = config['ks-pass']

    except:
        print('Please place `~/apkutil.json` containing the keystore information')
        return

    try:
        if not os.path.isfile(apk_path):
            errs = '{0} is not found.'.format(apk_path)
            raise Exception(errs)

        apksigner_path = glob.glob(home_dir + '/Library/Android/sdk/build-tools/*/apksigner')[0]
        apksigner_cmd = [apksigner_path]
        apksigner_cmd.append('sign')
        apksigner_cmd.extend(['-ks', keystore_path])
        apksigner_cmd.extend(['--v2-signing-enabled', 'true'])
        apksigner_cmd.append('-v')
        apksigner_cmd.extend(['--ks-key-alias', ks_key_alias])
        apksigner_cmd.extend(['--ks-pass', ks_pass])
        apksigner_cmd.append(apk_path)
        proc = subprocess.Popen(apksigner_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        outs, errs = proc.communicate()
        if (outs is not None) and (len(outs) != 0):
            print(Fore.CYAN + outs.decode('ascii'))
        
        if (errs is not None) and (len(errs) != 0):
            errs = errs.decode('ascii')
            raise Exception(errs)

    except (IndexError, FileNotFoundError) as e:
        print('apksigner not found.')
        print('Please install Android SDK Build Tools.')


def get_packagename(apk_path):
    try:
        home_dir = os.environ['HOME']
        aapt_path = glob.glob(home_dir + '/Library/Android/sdk/build-tools/*/aapt')[0]
        aapt_cmd = [aapt_path]
        aapt_cmd.append('l')
        aapt_cmd.append('-a')
        aapt_cmd.append(apk_path)
        aapt_proc = subprocess.Popen(aapt_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        grep_proc = subprocess.Popen(["grep", "A: package"], stdin=aapt_proc.stdout)
        aapt_proc.stdout.close()
        outs, errs = grep_proc.communicate()
        if (outs is not None) and (len(outs) != 0):
            print(outs.decode('ascii'))

        if (errs is not None) and (len(errs) != 0):
            errs = errs.decode('ascii')
            raise Exception(errs)

    except (IndexError, FileNotFoundError) as e:
        print('apksigner not found.')
        print('Please install Android SDK Build Tools.')


def get_screenshot():
    try:
        home_dir = os.environ['HOME']
        adb_path = glob.glob(home_dir + '/Library/Android/sdk/platform-tools/adb')[0]
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
        screenshot_file = 'screenshot-' + timestamp + '.png'
        screenshot_path = '/data/local/tmp/' + screenshot_file

        screencap_cmd = [adb_path]
        screencap_cmd.append('shell')
        screencap_cmd.append('screencap')
        screencap_cmd.extend(['-p', screenshot_path])
        screencap_proc = subprocess.Popen(screencap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, errs = screencap_proc.communicate()

        if (errs is not None) and (len(errs) != 0):
            errs = errs.decode('ascii')
            raise Exception(errs)

        pull_cmd = [adb_path]
        pull_cmd.append('pull')
        pull_cmd.append(screenshot_path)
        pull_proc = subprocess.Popen(pull_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        outs, errs = pull_proc.communicate()

        if (errs is not None) and (len(errs) != 0):
            errs = errs.decode('ascii')
            raise Exception(errs)

        if (outs is not None) and (len(outs) != 0):
            print(outs.decode('ascii'))

        rm_cmd = [adb_path]
        rm_cmd.append('shell')
        rm_cmd.append('rm')
        rm_cmd.append(screenshot_path)
        rm_proc = subprocess.Popen(rm_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, errs = rm_proc.communicate()
        if (errs is not None) and (len(errs) != 0):
            print(errs.decode('ascii'))

        return screenshot_file

    except (IndexError, FileNotFoundError) as e:
        print('adb not found.')
        print('Please install Android SDK Build Tools.')
