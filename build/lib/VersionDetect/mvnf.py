#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

# mvnForum version detection
# Rev 1

import cmseekdb.basic as cmseek
import re

def start(source):
    regex = re.search(r'Powered by(.*?)mvnForum (\d.*?)<\/a>', source)
    if regex != None:
        try:
            version = regex.group(2)
            cmseek.success('mvnForum version ' + cmseek.bold + cmseek.fgreen + version + cmseek.cln + ' detected')
            return version
        except Exception as e:
            cmseek.error('Version detection failed!')
            return '0'


    cmseek.error('Version detection failed!')
    return '0'
