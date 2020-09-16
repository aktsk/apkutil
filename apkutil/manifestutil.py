#!/usr/bin/env python3
# coding: UTF-8

import colorama
from colorama import Fore, Back, Style
import defusedxml.ElementTree as ET


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

    def get_custom_schemas(self):
        custom_schemas = []
        application_tag = self.root.findall('application')
        application_tag = application_tag[0]

        for activity_tag in application_tag.findall('activity'):
            for intent_filter_tag in activity_tag.findall('intent-filter'):
                for data_tag in intent_filter_tag.findall('data'):
                    if '{http://schemas.android.com/apk/res/android}scheme' in data_tag.attrib:
                        custom_schemas.append(data_tag.attrib['{http://schemas.android.com/apk/res/android}scheme'])
        
        return custom_schemas

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
            print(Fore.CYAN + p)
        print('')

        print('Debuggable:')
        if self.is_debuggable():
            print(Fore.RED + 'True' + '\n')
        else:
            print(Fore.BLUE + 'False' + '\n')

        print('AllowBackup:')
        if self.is_allowBackup():
            print(Fore.RED + 'True' + '\n')
        else:
            print(Fore.BLUE + 'False' + '\n')

        print('Custom schemas:')
        schemas = self.get_custom_schemas()
        if len(schemas) > 0:
            for schema in schemas:
                print(Fore.CYAN + schema)
        else:
            print(Fore.CYAN + 'None')

    def to_debuggable(self):
        application_tag = self.root.findall('application')
        application_tag = application_tag[0]
        application_tag.set('{http://schemas.android.com/apk/res/android}debuggable', 'true')
        self.tree.write(self.path)
