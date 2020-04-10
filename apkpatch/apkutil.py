#!/usr/bin/env python3
# coding: UTF-8

import glob
import json
import os
import subprocess


def decode(apk_name):
    apktool_cmd = ['apktool']
    apktool_cmd.extend(['d', apk_name])
    proc = subprocess.Popen(apktool_cmd, stdout=subprocess.PIPE)
    outs, errs = proc.communicate()
    print(outs.decode('ascii'))

def build(dir_name, apk_name):
    apktool_cmd = ['apktool']
    apktool_cmd.extend(['b', dir_name])
    apktool_cmd.extend(['-o', apk_name])
    proc = subprocess.Popen(apktool_cmd, stdout=subprocess.PIPE)
    outs, errs = proc.communicate()
    print(outs.decode('ascii'))

def sign(apk_name):
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
    apksigner_cmd.append(apk_name)
    proc = subprocess.Popen(apksigner_cmd, stdout=subprocess.PIPE)
    outs, errs = proc.communicate()
    print(outs.decode('ascii'))

