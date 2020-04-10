#!/usr/bin/env python3
# coding: UTF-8

import xml.etree.ElementTree as ET


class CheckManifest(object):

    def __init__(self, path):
        tree = ET.parse(path)
        self.root = tree.getroot()

    def get_permissions(self):
        permissions = []
        permissions_xml = self.root.findall("uses-permission")
        for perm in permissions_xml:
            for att in perm.attrib:
                permissions.append(perm.attrib[att])

        return permissions

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
