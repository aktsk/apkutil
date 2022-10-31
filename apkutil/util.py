#!/usr/bin/env python3
# coding: UTF-8

import datetime
import glob
import json
import os
import subprocess
import platform
import tempfile
from colorama import Fore

pf = platform.system()
if pf == 'Windows':
    popen_args = {'shell':True,'stdout':subprocess.PIPE,'stderr':subprocess.PIPE}
    apk_signer = 'apksigner.bat'
    zipalign = 'zipalign.exe'
    aapt = 'aapt.exe'
    adb = 'adb.exe'
elif pf == 'Darwin':
    popen_args = {'stdout':subprocess.PIPE,'stderr':subprocess.PIPE}
    apk_signer = 'apksigner'
    zipalign = 'zipalign'
    aapt = 'aapt'
    adb = 'adb'
elif pt == 'Linux':
    popen_args = {'stdout':subprocess.PIPE,'stderr':subprocess.PIPE}
    apk_signer = 'apksigner'
    zipalign = 'zipalign'
    aapt = 'aapt'
    adb = 'adb'

tmp_dir = tempfile.gettempdir()

def decode(apk_path, no_res=False, no_src=False):
    apktool_cmd = ['apktool']
    apktool_cmd.extend(['d', apk_path])

    if no_res:
        apktool_cmd.extend(['-r'])

    if no_src:
        apktool_cmd.extend(['-s'])

    try:
        proc = subprocess.Popen(apktool_cmd, **popen_args)
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


def build(dir_name, apk_path, aapt2=False):
    apktool_cmd = ['apktool']
    apktool_cmd.extend(['b', dir_name])
    apktool_cmd.extend(['-o', apk_path])

    if aapt2:
        apktool_cmd.extend(['--use-aapt2'])
    
    try:
        proc = subprocess.Popen(apktool_cmd, **popen_args)
        outs, errs = proc.communicate()

        is_built = False

        if (outs is not None) and (len(outs) != 0):
            outs = outs.decode('ascii')

            if "I: Built apk..." in outs:
                is_built = True

            print(outs)
        
        if (errs is not None) and (len(errs) != 0) and not is_built:
            errs = errs.decode('ascii')
            raise Exception(errs)

    except FileNotFoundError as e:
        print('apktool not found.')
        print('Please install apktool.')

def align(apk_path):
    android_home = os.environ['ANDROID_HOME'] or '/Library/Android/sdk/'

    try:
        zipalign_path = glob.glob(android_home + '/build-tools/*/' + zipalign)[0]
        zipalign_cmd = [zipalign_path]
        zipalign_cmd.append('-f')
        zipalign_cmd.extend(['-p', '4'])
        zipalign_cmd.append(apk_path)
        zipalign_cmd.append(tmp_dir + '/apkutil_tmp.aligned.apk')
        proc = subprocess.Popen(zipalign_cmd, **popen_args)
        _, errs = proc.communicate()
        if len(errs) != 0:
            errs = errs.decode('ascii')
            raise Exception(errs)

        os.replace(tmp_dir + '/apkutil_tmp.aligned.apk', apk_path)
    except (IndexError, FileNotFoundError) as e:
        print('zipalign not found.')
        print('Please install Android SDK Build Tools.')


def sign(apk_path):
    if pf == 'Windows':
        home_dir = os.environ['USERPROFILE']
    elif pf == 'Darwin':
        home_dir = os.environ['HOME']
    elif pf == 'Linux':
        home_dir = os.environ['HOME']        

    android_home = os.environ['ANDROID_HOME'] or '/Library/Android/sdk/'
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

        apksigner_path = glob.glob(android_home + '/build-tools/*/' + apk_signer)[0]
        apksigner_cmd = [apksigner_path]
        apksigner_cmd.append('sign')
        apksigner_cmd.extend(['-ks', keystore_path])
        apksigner_cmd.extend(['--v2-signing-enabled', 'true'])
        apksigner_cmd.append('-v')
        apksigner_cmd.extend(['--ks-key-alias', ks_key_alias])
        apksigner_cmd.extend(['--ks-pass', ks_pass])
        apksigner_cmd.append(apk_path)
        proc = subprocess.Popen(apksigner_cmd, **popen_args)
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
        android_home = os.environ['ANDROID_HOME'] or '/Library/Android/sdk/'
        aapt_path = glob.glob(android_home + '/build-tools/*/' + aapt)[0]
        aapt_cmd = [aapt_path]
        aapt_cmd.append('l')
        aapt_cmd.append('-a')
        aapt_cmd.append(apk_path)
        aapt_proc = subprocess.Popen(aapt_cmd, **popen_args)
        if pf == 'Windows':
            outs, errs = aapt_proc.communicate()
            for out in outs.split(b"\r\n"):
                if out.find(b"A: package") != -1:
                    print(out.decode('ascii'))
                    break
        else:
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
        android_home = os.environ['ANDROID_HOME'] or '/Library/Android/sdk/'
        adb_path = glob.glob(android_home + '/platform-tools/' + adb)[0]
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
        screenshot_file = 'screenshot-' + timestamp + '.png'
        screenshot_path = '/data/local/tmp/' + screenshot_file

        screencap_cmd = [adb_path]
        screencap_cmd.append('shell')
        screencap_cmd.append('screencap')
        screencap_cmd.extend(['-p', screenshot_path])
        screencap_proc = subprocess.Popen(screencap_cmd, **popen_args)
        _, errs = screencap_proc.communicate()

        if (errs is not None) and (len(errs) != 0):
            errs = errs.decode('ascii')
            raise Exception(errs)

        pull_cmd = [adb_path]
        pull_cmd.append('pull')
        pull_cmd.append(screenshot_path)
        pull_proc = subprocess.Popen(pull_cmd, **popen_args)
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
        rm_proc = subprocess.Popen(rm_cmd, **popen_args)
        _, errs = rm_proc.communicate()
        if (errs is not None) and (len(errs) != 0):
            print(errs.decode('ascii'))

        return screenshot_file

    except (IndexError, FileNotFoundError) as e:
        print('adb not found.')
        print('Please install Android SDK Build Tools.')


def check_sensitive_files(target_path):
    types = ('**/*.md', '**/*.cpp', '**/*.c', '**/*.h', '**/*.java', '**/*.kts',
        '**/*.bat', '**/*.sh', '**/*.template', '**/*.gradle', '**/*.json', '**/*.yml', '**/*.txt')
    allow_list = ('apktool.yml', '/assets/google-services-desktop.json',
        '/assets/bin/Data/RuntimeInitializeOnLoads.json', '/assets/bin/Data/ScriptingAssemblies.json')
    found_files = []
    for file_type in types:
        found_files.extend(glob.glob(os.path.join(target_path, file_type), recursive=True))
    
    sensitive_files = []
    for found_file in found_files:
        allow_flag = False
        for allow_file in allow_list:
            if found_file.endswith(allow_file):
                allow_flag = True
                break
        if not allow_flag:
            sensitive_files.append(found_file)

    if len(sensitive_files) == 0:
        print(Fore.BLUE + 'None')
    else:
        for sensitive_file in sensitive_files:
            print(Fore.RED + sensitive_file)
    print('')
    return sensitive_files

def make_network_security_config(target_path):
    xml_path = os.path.join(target_path, 'res/xml')
    if not os.path.exists(xml_path):
        os.makedirs(xml_path)

    with open(os.path.join(target_path, 'res/xml/network_security_config.xml'),'w') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n' +
            '<network-security-config>\n' +
            '    <base-config>\n' +
            '        <trust-anchors>\n' +
            '            <certificates src="system" />\n' +
            '            <certificates src="user" />\n' +
            '        </trust-anchors>\n' +
            '    </base-config>\n' +
            '</network-security-config>')
