#!/usr/bin/env python3
# coding: UTF-8

import datetime
import glob
import json
import os
import subprocess


def decode(apk_path):
    apktool_cmd = ['apktool']
    apktool_cmd.extend(['d', apk_path])
    proc = subprocess.Popen(apktool_cmd, stdout=subprocess.PIPE)
    outs, errs = proc.communicate()
    print(outs.decode('ascii'))

def build(dir_name, apk_path):
    apktool_cmd = ['apktool']
    apktool_cmd.extend(['b', dir_name])
    apktool_cmd.extend(['-o', apk_path])
    proc = subprocess.Popen(apktool_cmd, stdout=subprocess.PIPE)
    outs, errs = proc.communicate()
    print(outs.decode('ascii'))

def sign(apk_path):
    home_dir = os.environ['HOME']
    with open(home_dir + "/apkpatch.json") as f:
        config = json.load(f)
        keystore_path = config['keystore_path'].replace('~', home_dir)
        ks_key_alias = config['ks-key-alias']
        ks_pass = config['ks-pass']

    apksigner_path = glob.glob(home_dir + '/Library/Android/sdk/build-tools/*/apksigner')[0]
    apksigner_cmd = [apksigner_path]
    apksigner_cmd.append('sign')
    apksigner_cmd.extend(['-ks', keystore_path])
    apksigner_cmd.extend(['--v2-signing-enabled', 'true'])
    apksigner_cmd.append('-v')
    apksigner_cmd.extend(['--ks-key-alias', ks_key_alias])
    apksigner_cmd.extend(['--ks-pass', ks_pass])
    apksigner_cmd.append(apk_path)
    proc = subprocess.Popen(apksigner_cmd, stdout=subprocess.PIPE)
    outs, errs = proc.communicate()
    print(outs.decode('ascii'))

def get_packagename(apk_path):
    home_dir = os.environ['HOME']
    aapt_path = glob.glob(home_dir + '/Library/Android/sdk/build-tools/*/aapt')[0]
    aapt_cmd = [aapt_path]
    aapt_cmd.append('l')
    aapt_cmd.append('-a')
    aapt_cmd.append(apk_path)
    aapt_proc = subprocess.Popen(aapt_cmd, stdout=subprocess.PIPE)
    grep_proc = subprocess.Popen(["grep", "A: package"], stdin=aapt_proc.stdout, stdout=subprocess.PIPE)
    aapt_proc.stdout.close()
    outs, errs = grep_proc.communicate()
    print(outs.decode('ascii'))

def get_screenshot():
    home_dir = os.environ['HOME']
    adb_path = glob.glob(home_dir + '/Library/Android/sdk/platform-tools/adb')[0]
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    screenshot_path = '/data/local/tmp/screenshot-' + timestamp + '.png'

    screencap_cmd = [adb_path]
    screencap_cmd.append('shell')
    screencap_cmd.append('screencap')
    screencap_cmd.extend(['-p', screenshot_path])
    screencap_proc = subprocess.Popen(screencap_cmd, stdout=subprocess.PIPE)
    outs, errs = screencap_proc.communicate()

    pull_cmd = [adb_path]
    pull_cmd.append('pull')
    pull_cmd.append(screenshot_path)
    pull_proc = subprocess.Popen(pull_cmd, stdout=subprocess.PIPE)
    outs, errs = pull_proc.communicate()
    print(outs.decode('ascii'))

    rm_cmd = [adb_path]
    rm_cmd.append('shell')
    rm_cmd.append('rm')
    rm_cmd.append(screenshot_path)
    rm_proc = subprocess.Popen(rm_cmd, stdout=subprocess.PIPE)
    outs, errs = rm_proc.communicate()
