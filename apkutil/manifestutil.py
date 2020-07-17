#!/usr/bin/env python3
# coding: UTF-8

import colorama
from colorama import Fore, Back, Style
import xml.etree.ElementTree as ET


class ManifestUtil(object):

    def __init__(self, path):
        self.path = path
        self.tree = ET.parse(self.path)
        self.root = self.tree.getroot()

    def get_permissions(self):
        permissions = []
        permissions_xml = self.root.findall("uses-permission")
        for perm in permissions_xml:
            for att in perm.attrib:
                permissions.append(perm.attrib[att])

        return permissions

    def get_package_name(self):
        return self.root.attrib.get("package")


    def is_debuggable(self):
        application_tag = self.root.findall('application')
        application_tag = application_tag[0]
        if '{http://schemas.android.com/apk/res/android}debuggable' in application_tag.attrib \
                and application_tag.attrib['{http://schemas.android.com/apk/res/android}debuggable'] == 'true':
            return True

        else:
            return False

    def is_allowBackup(self):
        application_tag = self.root.findall('application')
        application_tag = application_tag[0]
        if '{http://schemas.android.com/apk/res/android}allowBackup' in application_tag.attrib \
                and application_tag.attrib['{http://schemas.android.com/apk/res/android}allowBackup'] == 'true':
            return True

        else:
            return False

    def check_all(self):
        colorama.init(autoreset=True)
        print('Package name:')
        print(Fore.CYAN + self.get_package_name() + '\n')

        print('Permission:')
        for p in self.get_permissions():
            print(p)
        print('')

        print('Debuggable:')
        if self.is_debuggable():
            print(Fore.RED + 'True' + '\n')
        else:
            print(Fore.BLUE + 'False' + '\n')

        print('AllowBackup:')
        if self.is_allowBackup():
            print(Fore.RED + 'True')
        else:
            print(Fore.BLUE + 'False')

    def to_debuggable(self):
        application_tag = self.root.findall('application')
        application_tag = application_tag[0]
        application_tag.set('{http://schemas.android.com/apk/res/android}debuggable', 'true')
        self.tree.write(self.path)
