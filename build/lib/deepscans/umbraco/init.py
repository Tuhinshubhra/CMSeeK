#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

# This is mostly for falsepositive detection

import cmseekdb.basic as cmseek ## Good old module
import VersionDetect.umbraco as umbraco_version_detect
import cmseekdb.result as sresult
import time
import os
import re

def falsepositive():
    cmseek.error('Detection was false positive! CMSeeK is quitting!')
    cmseek.success('Run CMSeeK with {0}{1}{2} argument next time'.format(cmseek.fgreen, '--ignore-cms umbraco', cmseek.cln))
    #cmseek.handle_quit()
    return

def start(id, url, ua, ga, source, detection_method, headers):
    if id == 'umbraco':
        cms_version = 0
        cmseek.statement('Starting Umbraco DeepScan')
        if detection_method == 'source':
            # detect if it's false positive
            umbraco_url = url + '/umbraco'
            test_src = cmseek.getsource(umbraco_url, ua)

            if test_src[0] == '1':
                # okay we got the source let's test it
                if 'var Umbraco' in test_src[1]:
                    # Umbraco Detected!
                    # Let's get version
                    cms_version = umbraco_version_detect.start(headers, url, ua, test_src[1])
                else:
                    falsepositive()
            else:
                falsepositive()
        else:
            # detection method was different so we are good and no need to check for false positive i guess
            cms_version = umbraco_version_detect.start(headers, url, ua)

        cmseek.clearscreen()
        cmseek.banner("CMS Scan Results")
        sresult.target(url)
        sresult.cms('Umbraco',cms_version,'https://umbraco.com')
        cmseek.update_log('cms_name', 'Umbraco') # update log
        if cms_version != '0' and cms_version != None:
            cmseek.update_log('cms_version', cms_version) # update log
        cmseek.update_log('cms_url', 'https://umbraco.com') # update log
        comptime = round(time.time() - cmseek.cstart, 2)
        log_file = os.path.join(cmseek.log_dir, 'cms.json')
        sresult.end(str(cmseek.total_requests), str(comptime), log_file)
        return
