#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

# YaBB version detection
# Rev 1

import cmseekdb.basic as cmseek
import re

def start(source):
    regex = re.search(r'Powered by(.*?)YaBB (\d.*?)( |</a>)', source, re.DOTALL)
    if regex != None:
        try:
            version = regex.group(2)
            cmseek.success('YaBB version ' + cmseek.bold + cmseek.fgreen + version + cmseek.cln + ' detected')
            return version
        except Exception as e:
            regex = re.findall(r'<!-- YaBB (\d.*?) ', source)
            if regex != []:
                if regex[0] != '' and regex[0] != ' ':
                    version = regex[0]
                    cmseek.success('YaBB version ' + cmseek.bold + cmseek.fgreen + version + cmseek.cln + ' detected')
                    return version
    else:
        regex = re.findall(r'<!-- YaBB (\d.*?) ', source)
        if regex != []:
            if regex[0] != '' and regex[0] != ' ':
                version = regex[0]
                cmseek.success('YaBB version ' + cmseek.bold + cmseek.fgreen + version + cmseek.cln + ' detected')
                return version

    cmseek.error('Version detection failed!')
    return '0'
