#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

# UMI.CMS Version detection
# Rev 1
import cmseekdb.basic as cmseek
import re

def start(url, ua):
    kurama = cmseek.getsource(url, ua) # was listening to https://soundcloud.com/ahmed-a-zidan/naruto-sad-music no better came to mind
    header = kurama[2].split('\n')
    regex = []
    for tail in header:
        if 'X-CMS-Version' in tail:
            regex = re.findall(r'X-CMS-Version: (.*)', tail)
    if regex != []:
        cmseek.success('UMI.CMS version ' + cmseek.bold + cmseek.fgreen + regex[0] + cmseek.cln + ' detected')
        return regex[0]
    else:
        cmseek.error('Version detection failed!')
        return '0'
