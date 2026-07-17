#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

# Commerce Server version detection
# Rev 1

import cmseekdb.basic as cmseek
import re

def start(url, ua):
    cmseek.statement('Detecting Commerce Server using headers [Method 1 of 1]')
    kurama = cmseek.getsource(url, ua)
    header = kurama[2].split('\n')
    regex = []
    for tail in header:
        if 'commerce-server-software:' in tail.lower():
            regex = re.findall(r'commerce-server-software: (.*)', tail, re.IGNORECASE)
    if regex != [] and regex[0] != "":
        cmseek.success('Commerce Server version ' + cmseek.bold + cmseek.fgreen + regex[0] + cmseek.cln + ' detected')
        return regex[0]
    else:
        cmseek.error('Version detection failed!')
        return '0'
