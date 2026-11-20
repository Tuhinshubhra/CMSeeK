#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 Tuhinshubhra

# Oracle ATG version detection
# Rev 1

import cmseekdb.basic as cmseek
import re
from base64 import b64decode


def start(headers):
    cmseek.statement('Detecting version using atg_version [Method 1 of 1]')
    try:
        encoded_version = re.search('X-ATG-Version: version=(.+)', headers).group(1)
        version = b64decode(encoded_version).decode('utf-8')
        version = re.search('ATGPlatform\/([\d\.]+)', version).group(1)
    except:
        version = None

    if version:
        cmseek.success('Oracle ATG version ' + cmseek.bold + version + cmseek.cln + ' detected')
    else:
        cmseek.error('Oracle ATG version detection failed!')
        version = '0'

    return version
