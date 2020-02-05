#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

# Quick.Cart version detection
# Rev 1

import cmseekdb.basic as cmseek
import re

def start(ga_content):
    cmseek.statement('Detecting Quick.Cart version using generator meta tag [Method 1 of 1]')
    regex = re.findall(r'Quick.Cart(.*?)v(.*)', ga_content)
    if regex != []:
        version = regex[0][1]
        cmseek.success('Quick.Cart version ' + cmseek.bold + cmseek.fgreen + version + cmseek.cln + ' detected')
        return version
    else:
        cmseek.error('Version detection failed!')
        return '0'
