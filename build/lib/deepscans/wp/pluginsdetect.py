#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

import cmseekdb.basic as cmseek
import re
import json

def start(source):
    cmseek.info('Starting passive plugin enumeration')
    plug_regex = re.compile('wp-content/plugins/([^/]+)/.+ver=([0-9\.]+)')
    results = plug_regex.findall(source)
    plugins = []
    found = 0
    for result in results:
        # found += 1
        name = result[0].replace('-master','').replace('.min','')
        nc = name + ":"
        if nc not in str(plugins):
            version = result[1]
            each_plugin = name + ":" + version
            plugins.append(each_plugin)
    plugins = set(plugins)
    found = len(plugins)
    if found > 0:
        if found == 1:
            cmseek.success(cmseek.bold + cmseek.fgreen + str(found) + " Plugin enumerated!")
        else:
            cmseek.success(cmseek.bold + cmseek.fgreen + str(found) + " Plugins enumerated!")
    else:
        cmseek.error('No plugins enumerated!')
    return [found, plugins]
