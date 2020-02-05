#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

# OpenText WSM version detection
# Rev 1

import cmseekdb.basic as cmseek
import re

def start(source):
    source = source.lower()
    regex = re.findall(r'published by open text web solutions (.*?) -->', source)
    if regex != []:
        version = regex[0]
        if '-' in version:
            version = version.split('-')
            version = version[1].replace(' ', '')
        cmseek.success('OpenText WSM version ' + cmseek.bold + cmseek.fgreen + version + cmseek.cln + ' detected')
        return version
    else:
        cmseek.error('Version detection failed!')
        return '0'
