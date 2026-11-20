#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

# Drupal version detection
# Rev 1
import cmseekdb.basic as cmseek
import re
def start(id, url, ua, ga, source):
    if ga == '1':
        # well for now we only have one way of detecting the version - Not any more!
        cmseek.statement('Detecting version using generator meta tag [Method 1 of 2]')
        regex = re.findall(r'<meta name="Generator" content="Drupal (.*?) \(http(s|):\/\/(www\.|)drupal.org\)"', source)
        if regex != []:
            cmseek.success('Drupal version ' + cmseek.bold + regex[0][0] + cmseek.cln + ' detected')
            return regex[0][0]
    else:
        # Detect version via CHANGELOG.txt (not very accurate)
        cmseek.statement('Detecting version using CHANGELOG.txt [Method 2 of 2]')
        changelog = url + '/CHANGELOG.txt'
        changelog_source = cmseek.getsource(changelog, ua)
        if changelog_source[0] == '1' and 'Drupal' in changelog_source[1]:
            cl_array = changelog_source[1].split('\n')
            for line in cl_array:
                match = re.findall(r'Drupal (.*?),', line)
                if match != []:
                    cmseek.success('Drupal version ' + cmseek.bold + match[0] + cmseek.cln + ' detected')
                    return match[0]
            cmseek.error('Drupal version detection failed!')
            return '0'
        else:
            cmseek.error('Drupal version detection failed!')
            return '0'
    return '0'
