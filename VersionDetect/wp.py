#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

## WordPress version detection
## Rev 1

import cmseekdb.basic as cmseek
import re

def start(id, url, ua, ga, source):
    version = '0'
    cmseek.statement('Detecting Version and vulnerabilities')
    if ga == '1' or ga == '2' or ga == '3': ## something good was going to happen but my sleep messed it up TODO: will fix it later
        cmseek.statement('Generator Tag Available... Trying version detection using generator meta tag')
        rr = re.findall(r'<meta name=\"generator\" content=\"WordPress (.*?)\"', source)
        if rr != []:
            version = rr[0]
            cmseek.success(cmseek.bold + cmseek.fgreen + "Version Detected, WordPress Version %s" % version + cmseek.cln)
        else:
            cmseek.warning("Generator tag was a big failure.. looking up /feed/")
            fs = cmseek.getsource(url + '/feed/', ua)
            if fs[0] != '1': # Something messed up real bad
                cmseek.warning("Couldn't get feed source code, Error: %s" % fs[1])
            else:
                fv = re.findall(r'<generator>https://wordpress.org/\?v=(.*?)</generator>', fs[1])
                if fv != []: # Not empty good news xD
                    version = fv[0]
                    cmseek.success(cmseek.bold + cmseek.fgreen + "Version Detected, WordPress Version %s" % version + cmseek.cln)
                else:
                    cmseek.warning("Well even feed was a failure... let's lookup wp-links-opml then")
                    opmls = cmseek.getsource(url + '/wp-links-opml.php', ua)
                    if opmls[0] != '1': # Something messed up real bad
                        cmseek.warning("Couldn't get wp-links-links source code, Error: %s" % opmls[1])
                    else:
                        fv = re.findall(r'generator=\"wordpress/(.*?)\"', opmls[1])
                        if fv != []: # Not empty good news xD || you can guess it's copied right?
                            version = fv[0]
                            cmseek.success(cmseek.bold + cmseek.fgreen + "Version Detected, WordPress Version %s" % version + cmseek.cln)
                        else:
                            ## new version detection methods will be added in the future updates
                            cmseek.error("Couldn't Detect Version") #sorry master thingy removed... sounded kinda cheesy -_-
                            version = '0'
    return version
