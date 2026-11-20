#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

import cmseekdb.basic as cmseek
import re

def start(source,url,ua):
    cmseek.info('Starting passive theme enumeration')
    ## plug_file = open('database/themes.json', 'r')
    ## plug_data = plug_file.read()
    ## plug_json = json.loads(plug_data)
    plug_regex = re.compile('wp-content/themes/([^/]+)/.+ver=([0-9\.]+)')
    results = plug_regex.findall(source)
    themes = []
    found = 0
    for result in results:
        # found += 1
        name = result[0].replace('-master','').replace('.min','')
        nc = name + ":"
        if nc not in str(themes):
            version = result[1]
            each_theme = name + ":" + version + "|"
            # look if theme zip available
            cmseek.statement('Looking for theme zip file!')
            theme_zip = url + '/wp-content/themes/' + name + '.zip'
            zip_status = cmseek.check_url(theme_zip, ua)
            if zip_status == '1':
                cmseek.success('Current theme can be downloaded, URL: ' + cmseek.bold + theme_zip + cmseek.cln)
                each_theme += '/wp-content/themes/' + name + '.zip'
            themes.append(each_theme)
    themes = set(themes)
    found = len(themes)
    if found > 0:
        if found == 1:
            cmseek.success(cmseek.bold + cmseek.fgreen + str(found) + " theme detected!")
        else:
            cmseek.success(cmseek.bold + cmseek.fgreen + str(found) + " themes detected!")
    else:
        cmseek.error('Could not detect theme!')
    return [found, themes]
