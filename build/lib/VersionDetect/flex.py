#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

# FlexCMP version detection
# Rev 1

import cmseekdb.basic as cmseek
import re

def start(source, url, ua):
    regex = re.findall(r'<!--.*-->', source, re.DOTALL)
    if regex != []:
        for r in regex:
            if 'FlexCMP' in r and 'v.' in r:
                tmp = r.split('\n')
                for t in tmp:
                    if 'v.' in t:
                        kek = re.findall(r'v. (.*?) -', t)
                        if kek != []:
                            # coding this was actually fun idk why ;--;
                            version = kek[0]
                            cmseek.success('FlexCMP version ' + cmseek.bold + cmseek.fgreen + version + cmseek.cln + ' detected from source')
                            return version
    else:
        kurama = cmseek.getsource(url, ua)
        header = kurama[2].split('\n')
        regex = []
        for tail in header:
            if 'X-Powered-By' in tail and 'FlexCMP' in tail:
                regex = re.findall(r'X-Powered-By: FlexCMP Application Server \[v\. (.*?) - ', tail)
        if regex != []:
            cmseek.success('FlexCMP version ' + cmseek.bold + cmseek.fgreen + regex[0] + cmseek.cln + ' detected from header')
            return regex[0]
        else:
            cmseek.error('Version detection failed!')
            return '0'
