#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

# XpressEngine version detection
# Rev 1
import cmseekdb.basic as cmseek
import re

def start(ga_content):
    regex = re.findall(r'XpressEngine (.*)', ga_content)
    if regex != []:
        cmseek.success('XpressEngine version ' + cmseek.bold + cmseek.fgreen + regex[0] + cmseek.cln + ' detected')
        return regex[0]
    else:
        cmseek.error('Version detection failed!')
        return '0'
