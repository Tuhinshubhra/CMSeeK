#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

# CMSimple version detection
# Rev 1

import cmseekdb.basic as cmseek
import re

def start(ga_content):
    ga_content = ga_content.lower()
    if 'cmsimple_' in ga_content:
        regex = re.search(r'cmsimple_(.*?) (.*?) ', ga_content)
        if regex != []:
            try:
                version = regex.group(2)
                cmseek.success('CMSimple version ' + cmseek.bold + cmseek.fgreen + version + cmseek.cln + ' detected')
                return version
            except Exception as e:
                    cmseek.error('Version detection failed!')
                    return '0'
    else:
        regex = re.findall(r'cmsimple (.*)', ga_content)
        if regex != []:
            version = regex[0]
            cmseek.success('CMSimple version ' + cmseek.bold + cmseek.fgreen + version + cmseek.cln + ' detected')
        return version

    cmseek.error('Version detection failed!')
    return '0'
