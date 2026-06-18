#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 Tuhinshubhra

# Umbraco version detection
# Rev 1

import cmseekdb.basic as cmseek
import re

def start(headers, url, ua, temp_src=''):
    cmseek.statement('Detecting Umbraco using headers [Method 1 of 2]')
    header = headers.split('\n')
    regex = []
    for tail in header:
        if 'x-umbraco-version:' in tail.lower():
            regex = re.findall(r'X-Umbraco-Version: (.*)', tail, re.IGNORECASE)

    if regex != [] and regex[0] != "":
        # detection via headers successful
        cmseek.success('Umbraco version ' + cmseek.bold + cmseek.fgreen + regex[0] + cmseek.cln + ' detected')
        return regex[0]
    else:
        cmseek.statement('Detecting Umbraco using source code [Method 2 of 2]')
        if temp_src == '':
            # no additional source code sent so we have to get it
            temp_url = url + '/umbraco'
            temp_src = cmseek.getsource(temp_url, ua)
            if temp_src[0] == '1':
                temp_src = temp_src[1]
            else:
                cmseek.error('Version detection failed!')
                return '0'

        new_regex = re.findall('"version"\: "(.*?)"', temp_src)

        if new_regex != [] and new_regex[0] != "":
            # detection via headers successful
            cmseek.success('Umbraco version ' + cmseek.bold + cmseek.fgreen + new_regex[0] + cmseek.cln + ' detected')
            return new_regex[0]
        else:
            cmseek.error('Version detection failed!')
            return '0'
