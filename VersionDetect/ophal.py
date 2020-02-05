#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

# Ophal version detection
# Rev 1

import cmseekdb.basic as cmseek
import re

def start(ga_content, url, ua):
    ga_content = ga_content.lower()
    regex = re.findall(r'ophal (.*?) \(ophal.org\)', ga_content)
    if regex != []:
        version = regex[0]
        cmseek.success('Ophal version ' + cmseek.bold + cmseek.fgreen + version + cmseek.cln + ' detected')
        return version
    else:
        kurama = cmseek.getsource(url, ua) # copypasta
        header = kurama[2].split('\n')
        regex = []
        for tail in header:
            if 'x-powered-by' in tail:
                regex = re.findall(r'x-powered-by: Ophal (.*?) \(ophal.org\)', tail)
        if regex != []:
            cmseek.success('Ophal version ' + cmseek.bold + cmseek.fgreen + regex[0] + cmseek.cln + ' detected')
            return regex[0]
        else:
            cmseek.error('Version detection failed!')
            return '0'
