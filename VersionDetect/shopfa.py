#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

# ShopFA version detection
# Rev 1

import cmseekdb.basic as cmseek
import re

def start(ga_content, header):
    cmseek.statement('Detecting ShopFA version using generator meta tag [Method 1 of 2]')
    regex = re.findall(r'ShopFA (.*)', ga_content)
    if regex != []:
        version = regex[0]
        cmseek.success('ShopFA version ' + cmseek.bold + cmseek.fgreen + version + cmseek.cln + ' detected')
        return version
    else:
        cmseek.statement('Detecting ShopFA version using HTTP Headers [Method 2 of 2]')
        headers = header.split('\n')
        regex = []
        for h in headers:
            if 'X-Powered-By: ShopFA' in h:
                regex = re.findall(r'X-Powered-By: ShopFA (.*)', h)
        if regex != []:
            version = regex[0]
            cmseek.success('ShopFA version ' + cmseek.bold + cmseek.fgreen + version + cmseek.cln + ' detected')
            return version
        else:
            cmseek.error('Version detection failed!')
            return '0'
