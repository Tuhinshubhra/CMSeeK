#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

# SULU Version detection
# Rev 1
import cmseekdb.basic as cmseek
import re

def start(url, ua):
    kurama = cmseek.getsource(url, ua)
    header = kurama[2].split('\n')
    regex = []
    for tail in header:
        if 'x-generator' in tail:
            regex = re.findall(r'x-generator: Sulu/(.*)', tail)
    if regex != []:
        cmseek.success('SULU version ' + cmseek.bold + cmseek.fgreen + regex[0] + cmseek.cln + ' detected')
        return regex[0]
    else:
        cmseek.error('Version detection failed!')
        return '0'
