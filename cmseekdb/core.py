#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

## Core Rev 4, stable, strong and accurate

import sys
import os
import http.client
import urllib.request
import json
import importlib
from datetime import datetime
import time

import VersionDetect.detect as version_detect # Version detection
import deepscans.core as advanced # Deep scan and Version Detection functions
import cmseekdb.basic as cmseek # All the basic functions
import cmseekdb.sc as source # Contains function to detect cms from source code
import cmseekdb.header as header # Contains function to detect CMS from gathered http headers
import cmseekdb.cmss as cmsdb # Contains basic info about the CMSs
import cmseekdb.robots as robots
import cmseekdb.generator as generator
import cmseekdb.result as result

def main_proc(site,cua):

    # Check for skip_scanned
    if cmseek.skip_scanned:
        for csite in cmseek.report_index['results'][0]:
            if site == csite and cmseek.report_index['results'][0][site]['cms_id'] != '':
                cmseek.warning('Skipping {0} as it was previously scanned!'.format(cmseek.red + site + cmseek.cln))
                return

    cmseek.clearscreen()
    cmseek.banner("CMS Detection And Deep Scan")
    cmseek.info("Scanning Site: " + site)
    cmseek.statement("User Agent: " + cua)
    cmseek.statement("Collecting Headers and Page Source for Analysis")
    init_source = cmseek.getsource(site, cua)
    if init_source[0] != '1':
        cmseek.error("Aborting CMSeek! Couldn't connect to site \n    Error: %s" % init_source[1])
        return
    else:
        scode = init_source[1]
        headers = init_source[2]
        if site != init_source[3] and site + '/' != init_source[3]:
            if cmseek.redirect_conf == '0':
                cmseek.info('Target redirected to: ' + cmseek.bold + cmseek.fgreen + init_source[3] + cmseek.cln)
                if not cmseek.batch_mode:
                    follow_redir = input('[#] Set ' + cmseek.bold + cmseek.fgreen + init_source[3] + cmseek.cln + ' as target? (y/n): ')
                else:
                    follow_redir = 'y'
                if follow_redir.lower() == 'y':
                    site = init_source[3]
                    cmseek.statement("Reinitiating Headers and Page Source for Analysis")
                    tmp_req = cmseek.getsource(site, cua)
                    scode = tmp_req[1]
                    headers = tmp_req[2]
            elif cmseek.redirect_conf == '1':
                site = init_source[3]
                cmseek.info("Followed redirect, New target: " + cmseek.bold + cmseek.fgreen + init_source[3] + cmseek.cln)
                cmseek.statement("Reinitiating Headers and Page Source for Analysis")
                tmp_req = cmseek.getsource(site, cua)
                scode = tmp_req[1]
                headers = tmp_req[2]
            else:
                cmseek.statement("Skipping redirect to " + cmseek.bold + cmseek.red + init_source[3] + cmseek.cln)
    if scode == '':
        # silly little check thought it'd come handy
        cmseek.error('Aborting detection, source code empty')
        return

    cmseek.statement("Detection Started")

    ## init variables
    cms = '' # the cms id if detected
    cms_detected = '0' # self explanotory
    detection_method = '' # ^
    ga = '0' # is generator available
    ga_content = '' # Generator content

    ## Parse generator meta tag
    parse_generator = generator.parse(scode)
    ga = parse_generator[0]
    ga_content = parse_generator[1]

    cmseek.statement("Using headers to detect CMS (Stage 1 of 4)")
    header_detection = header.check(headers)

    if header_detection[0] == '1':
        detection_method = 'header'
        cms = header_detection[1]
        cms_detected = '1'

    if cms_detected == '0':
        if ga == '1':
            # cms detection via generator
            cmseek.statement("Using Generator meta tag to detect CMS (Stage 2 of 4)")
            gen_detection = generator.scan(ga_content)
            if gen_detection[0] == '1':
                detection_method = 'generator'
                cms = gen_detection[1]
                cms_detected = '1'
        else:
            cmseek.statement('Skipping stage 2 of 4: No Generator meta tag found')

    if cms_detected == '0':
        # Check cms using source code
        cmseek.statement("Using source code to detect CMS (Stage 3 of 4)")
        source_check = source.check(scode, site)
        if source_check[0] == '1':
            detection_method = 'source'
            cms = source_check[1]
            cms_detected = '1'

    if cms_detected == '0':
        # Check cms using robots.txt
        cmseek.statement("Using robots.txt to detect CMS (Stage 4 of 4)")
        robots_check = robots.check(site, cua)
        if robots_check[0] == '1':
            detection_method = 'robots'
            cms = robots_check[1]
            cms_detected = '1'

    if cms_detected == '1':
        cmseek.success('CMS Detected, CMS ID: ' + cmseek.bold + cmseek.fgreen + cms + cmseek.cln + ', Detection method: ' + cmseek.bold + cmseek.lblue + detection_method + cmseek.cln)
        cmseek.update_log('detection_param', detection_method)
        cmseek.update_log('cms_id', cms) # update log
        cmseek.statement('Getting CMS info from database') # freaking typo
        cms_info = getattr(cmsdb, cms)
        
        if cms_info['deeps'] == '1' and not cmseek.light_scan and not cmseek.only_cms:
            # cmseek.success('Starting ' + cmseek.bold + cms_info['name'] + ' deep scan' + cmseek.cln)
            advanced.start(cms, site, cua, ga, scode, ga_content, detection_method, headers)
            return
        
        elif cms_info['vd'] == '1' and not cmseek.only_cms:
            cmseek.success('Starting version detection')
            cms_version = '0' # Failsafe measure
            cms_version = version_detect.start(cms, site, cua, ga, scode, ga_content, headers)
            cmseek.clearscreen()
            cmseek.banner("CMS Scan Results")
            result.target(site)
            result.cms(cms_info['name'],cms_version,cms_info['url'])
            cmseek.update_log('cms_name', cms_info['name']) # update log
            if cms_version != '0' and cms_version != None:
                cmseek.update_log('cms_version', cms_version) # update log
            cmseek.update_log('cms_url', cms_info['url']) # update log
            comptime = round(time.time() - cmseek.cstart, 2)
            log_file = os.path.join(cmseek.log_dir, 'cms.json')
            result.end(str(cmseek.total_requests), str(comptime), log_file)
            '''
            cmseek.result('Target: ', site)
            cmseek.result("Detected CMS: ", cms_info['name'])
            cmseek.update_log('cms_name', cms_info['name']) # update log
            if cms_version != '0' and cms_version != None:
                cmseek.result("CMS Version: ", cms_version)
                cmseek.update_log('cms_version', cms_version) # update log
            cmseek.result("CMS URL: ", cms_info['url'])
            cmseek.update_log('cms_url', cms_info['url']) # update log
            '''
            return
        else:
            # nor version detect neither DeepScan available
            cmseek.clearscreen()
            cmseek.banner("CMS Scan Results")
            result.target(site)
            result.cms(cms_info['name'],'0',cms_info['url'])
            cmseek.update_log('cms_name', cms_info['name']) # update log
            cmseek.update_log('cms_url', cms_info['url']) # update log
            comptime = round(time.time() - cmseek.cstart, 2)
            log_file = os.path.join(cmseek.log_dir, 'cms.json')
            result.end(str(cmseek.total_requests), str(comptime), log_file)
            '''
            cmseek.result('Target: ', site)
            cmseek.result("Detected CMS: ", cms_info['name'])
            cmseek.update_log('cms_name', cms_info['name']) # update log
            cmseek.result("CMS URL: ", cms_info['url'])
            cmseek.update_log('cms_url', cms_info['url']) # update log
            '''
            return
    else:
        print('\n')
        cmseek.error('CMS Detection failed, if you know the cms please help me improve CMSeeK by reporting the cms along with the target by creating an issue')
        print('''
{2}Create issue:{3} https://github.com/Tuhinshubhra/CMSeeK/issues/new

{4}Title:{5} [SUGGESTION] CMS detction failed!
{6}Content:{7}
    - CMSeeK Version: {0}
    - Target: {1}
    - Probable CMS: <name and/or cms url>

N.B: Create issue only if you are sure, please avoid spamming!
        '''.format(cmseek.cmseek_version, site, cmseek.bold, cmseek.cln, cmseek.bold, cmseek.cln, cmseek.bold, cmseek.cln))
        return
    return
