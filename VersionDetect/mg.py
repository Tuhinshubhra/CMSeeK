#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

# Magento version detection
# Rev 1
import cmseekdb.basic as cmseek
import re
def start(url, ua):
    # Detect version via magento_version (not very accurate)
    cmseek.statement('Detecting version using magento_version [Method 1 of 1]')
    magento_version = url + '/magento_version'
    changelog_source = cmseek.getsource(magento_version, ua)
    if changelog_source[0] == '1' and 'Magento' in changelog_source[1]:
        cl_array = changelog_source[1].split('/')
        if cl_array != []:
            cmseek.success('Magento version ' + cmseek.bold + cl_array[1] + cmseek.cln + ' detected')
            return cl_array[1]
        cmseek.error('Magento version detection failed!')
        return '0'
    else:
        cmseek.error('Magento version detection failed!')
        return '0'