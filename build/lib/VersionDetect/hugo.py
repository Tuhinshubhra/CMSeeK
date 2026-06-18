#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2022 Konstantin Shibkov

## Hugo version detection
## Rev 1

import cmseekdb.basic as cmseek
import re

def start(source):
    version = '0'
    cmseek.statement('Detecting Version')
    cmseek.statement('Generator Tag Available... Trying version detection using generator meta tag')
    rr = re.findall(r'<meta name=[\"]*generator[\"]* content=\"Hugo (.*?)\"', source)
    if rr != []:
        version = rr[0]
        cmseek.success(cmseek.bold + cmseek.fgreen + "Version Detected, Hugo Version %s" % version + cmseek.cln)
    return version
