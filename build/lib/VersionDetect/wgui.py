#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

# WebGUI version detection
# Rev 1

import cmseekdb.basic as cmseek
import re

def start(ga_content):
    regex = re.findall(r'WebGUI (.*)', ga_content)
    if regex != []:

        if ')' in regex[0]:
            # This could be done by regex right? if you know how to do so proudly create an issue and show me the way ;)
            version = regex[0].replace(')','')
        else:
            version = regex[0]

        cmseek.success('WebGUI version ' + cmseek.bold + cmseek.fgreen + version + cmseek.cln + ' detected')
        return version
    else:
        cmseek.error('Version detection failed!')
        return '0'
