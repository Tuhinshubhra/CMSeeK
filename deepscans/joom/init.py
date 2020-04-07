#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

# Joomla DeepScan
# Rev 1
# Props to joomscan.. big time! https://github.com/rezasp/joomscan

import os
import cmseekdb.basic as cmseek
import VersionDetect.joom as version_detect
import deepscans.joom.backups as backup_finder
import deepscans.joom.config_leak as config_check
import deepscans.joom.core_vuln as core_vuln
import deepscans.joom.admin_finder as admin_finder
import deepscans.joom.check_debug as check_debug
import deepscans.joom.dir_list as dir_list
import deepscans.joom.check_reg as user_registration

def start(id, url, ua, ga, source):

    # Remove / from url
    if url.endswith("/"):
        url = url[:-1]

    # init variables
    vuln_detection = '0'
    vuln_count = 0
    joom_vulns = []

    # Version Detection
    version = version_detect.start(id, url, ua, ga, source)

    # Detecting joomla core vulnerabilities
    jcv = core_vuln.start(version)
    vuln_detection = jcv[0]
    vuln_count = jcv[1]
    joom_vulns = jcv[2]

    # README.txt
    readmesrc = cmseek.getsource(url + '/README.txt', ua)
    if readmesrc[0] != '1': ## something went wrong while getting the source codes
        cmseek.statement("Couldn't get readme file's source code most likely it's not present")
        readmefile = '0'
    elif 'This is a Joomla!' in readmesrc[1]:
        cmseek.info('README.txt file found')
        readmefile = '1' # Readme file present
    else:
        readmefile = '2' # Readme file found but most likely it's not of joomla

    # Debug Mode
    cmseek.info('Checking debug mode status')
    debug_mode = check_debug.start(source)

    # Check user registration status
    cmseek.statement('Checking if user registration is enabled')
    registration = user_registration.start(url,ua)

    # Find admin url
    cmseek.info('Locating admin url')
    admin = admin_finder.start(url,ua)

    # Backups check
    cmseek.info('Checking for common Backups')
    backups = backup_finder.start(url,ua)

    # Check Potential configuration file leak
    cmseek.info('Looking for potential config leak')
    configs = config_check.start(url,ua)

    # Checking for directory listing
    cmseek.statement('Checking for directory listing')
    directories = dir_list.start(url, ua)

    ### THE RESULTS START FROM HERE

    cmseek.clearscreen()
    cmseek.banner("Deep Scan Results")
    cmseek.result('Target: ',url)
    cmseek.result("Detected CMS: ", 'Joomla')
    cmseek.update_log('cms_name','joomla') # update log
    cmseek.result("CMS URL: ", "https://joomla.org")
    cmseek.update_log('cms_url', "https://joomla.org") # update log

    if version != '0':
        cmseek.result("Joomla Version: ", version)
        cmseek.update_log('joomla_version', version)

    if registration[0] == '1':
        cmseek.result('User registration enabled: ', registration[1])
        cmseek.update_log('user_registration_url', registration[1])

    if debug_mode =='1':
        cmseek.result('Debug mode enabled', '')
        cmseek.update_log('joomla_debug_mode', 'enabled')
    else:
        cmseek.update_log('joomla_debug_mode', 'disabled')

    if readmefile == '1':
        cmseek.result('Readme file: ', url + '/README.txt')
        cmseek.update_log('joomla_readme_file', url + '/README.txt')

    if admin[0] > 0:
        cmseek.result('Admin URL: ', url + admin[1][0])
        admin_log = ''
        for adm in admin[1]:
            admin_log += url + '/' + adm + ','
            # print(cmseek.bold + cmseek.fgreen + "   [B] " + cmseek.cln + url + '/' + adm)
        cmseek.update_log('joomla_backup_files', admin_log)
        print('\n')

    if directories[0] > 0:
        cmseek.result('Open directories: ', str(directories[0]))
        cmseek.success('Open directory url: ')
        dirs = ''
        for dir in directories[1]:
            dirs += url + '/' + dir + ','
            print(cmseek.bold + cmseek.fgreen + "   [>] " + cmseek.cln + url + dir)
        cmseek.update_log('directory_listing', dirs)
        print('\n')

    if backups[0] > 0:
        cmseek.result('Found potential backup file: ', str(backups[0]))
        cmseek.success('Backup URLs: ')
        bkup_log = []
        for backup in backups[1]:
            bkup_log.append(url + '/' + backup)
            print(cmseek.bold + cmseek.fgreen + "   [B] " + cmseek.cln + url + '/' + backup)
        cmseek.update_log('joomla_backup_files', bkup_log, False)
        print('\n')

    if configs[0] > 0:
        cmseek.result('Found potential Config file: ', str(configs[0]))
        cmseek.success('Config URLs: ')
        conf_log = ''
        for config in configs[1]:
            conf_log += url + '/' + config + ','
            print(cmseek.bold + cmseek.fgreen + "   [c] " + cmseek.cln + url + '/' + config)
        cmseek.update_log('joomla_config_files', conf_log)
        print('\n')

    if vuln_detection == '1' and vuln_count > 0:
        cmseek.result('Total joomla core vulnerabilities: ', str(vuln_count))
        cmseek.update_log("vulnerabilities_count", vuln_count)
        joomla_vulns_to_log = []
        cmseek.info('Vulnerabilities found: \n')
        for vuln in joom_vulns:
            # prepare the vuln details to be added to the log
            _vulnName = vuln.split('\\n')[0]
            _vulnRefs = []
            # TODO: try not to use a for loop here.
            for _index, _vr in enumerate(vuln.split('\\n')):
                if _index != 0:
                    _vulnRefs.append(_vr)
            
            joomla_vulns_to_log.append({"name": _vulnName, "references": _vulnRefs})
            vuln = vuln.replace('\\n', cmseek.cln + '\n    ')
            print(cmseek.bold + cmseek.red + '[v] ' + vuln)
            print('\n')
        cmseek.update_log("vulnerabilities", joomla_vulns_to_log, False)
    elif vuln_detection == '2':
        cmseek.update_log("vulnerabilities_count", 0)
        cmseek.warning('Couldn\'t find core vulnerabilities, No VERSION detected')
    elif vuln_detection == '3':
        cmseek.update_log("vulnerabilities_count", 0)
        cmseek.error('Core vulnerability database not found!')
    else:
        cmseek.update_log("vulnerabilities_count", 0)
        cmseek.warning('No core vulnerabilities detected!')
