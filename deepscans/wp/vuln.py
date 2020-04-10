#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

import cmseekdb.basic as cmseek
import json

def start(version,ua):
    if version == "0":
        cmseek.warning("Skipping version vulnerability scan as WordPress Version wasn't detected")
        wpvdbres = '0' # fix for issue #3
        result = ""
        vfc = ""
    else: ## So we have a version let's scan for vulnerabilities
        cmseek.info("Checking version vulnerabilities using wpvulns.com")
        vfc = version.replace('.','') # NOT IMPORTANT: vfc = version for check well we have to kill all the .s in the version for looking it up on wpvulndb.. kinda weird if you ask me
        #ws = cmseek.getsource("https://wpvulndb.com/api/v2/wordpresses/" + vfc, ua)
        # print(ws[0])
        ws = cmseek.getsource("https://wpvulns.com/version/{0}.json".format(version), ua)
        if ws[0] == "1":
            # wjson = json.loads(ws[1]) + vfd + "['release_date']"
            wpvdbres = '1' ## We have the wpvulndb results
            result = json.loads(ws[1]) #[version]
        else:
            wpvdbres = '0'
            result = ""
            cmseek.error('Error Retriving data from wpvulndb')
    return [wpvdbres, result, vfc]
