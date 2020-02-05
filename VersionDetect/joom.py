#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

## Joomla version detection
## Rev 1

import cmseekdb.basic as cmseek
import re
def start(id, url, ua, ga, source):
    version = '0'
    cmseek.info('detecting joomla version')

    # version detection stats here
    if ga == '1':
        # Detect version via generator meta tag
        cmseek.statement('Detecting version using generator meta tag [Method 1 of 4]')
        regex_1 = re.findall(r'content=(?:\"|\')Joomla! (.*?) - Open Source Content Management(?:\"|\')', source)
        if regex_1 != []:
            cmseek.success('Joomla version detected, version: ' + cmseek.bold + regex_1[0] + cmseek.cln)
            return regex_1[0]

    if version == '0':
        # Detections using the xml files
        xml_files = ['administrator/manifests/files/joomla.xml','language/en-GB/en-GB.xml','administrator/components/com_content/content.xml','administrator/components/com_plugins/plugins.xml','administrator/components/com_media/media.xml','mambots/content/moscode.xml']
        cmseek.statement('Detecting version using xml files [Method 2 of 4]')
        for xml_file in xml_files:
            xml_source = cmseek.getsource(url + '/' + xml_file, ua)
            if xml_source[0] == '1':
                regex_2 = re.findall(r'<version>(.*?)</version>', xml_source[1])
                if regex_2 != []:
                    cmseek.success('Joomla version detected, version: ' + cmseek.bold + regex_2[0] + cmseek.cln)
                    return regex_2[0]

    # Detection method 3
    if version == '0':
        other_files = ['language/en-GB/en-GB.xml','templates/system/css/system.css','media/system/js/mootools-more.js','language/en-GB/en-GB.ini','htaccess.txt','language/en-GB/en-GB.com_media.ini']
        cmseek.statement('Detecting version using advanced fingerprinting [Method 3 of 4]')
        for file in other_files:
            file_source = cmseek.getsource(url + '/' + file, ua)
            if file_source[0] == '1':
                # Regex find
                regex_3 = re.findall(r'<meta name="Keywords" content="(.*?)">', file_source[1])
                if regex_3 != []:
                    cmseek.success('Joomla version detected, version: ' + cmseek.bold + regex_3[0] + cmseek.cln)
                    return regex_3[0]

                # Joomla version 1.6
                j16 = ['system.css 20196 2011-01-09 02:40:25Z ian','MooTools.More={version:"1.3.0.1"','en-GB.ini 20196 2011-01-09 02:40:25Z ian','en-GB.ini 20990 2011-03-18 16:42:30Z infograf768','20196 2011-01-09 02:40:25Z ian']
                for j in j16:
                    rsearch = re.search(j,file_source[1])
                    if rsearch is not None:
                        cmseek.success('Joomla version detected, version: ' + cmseek.bold + '1.6' + cmseek.cln)
                        return '1.6'

                # Joomla version 1.5
                j15 = ['Joomla! 1.5','MooTools={version:\'1.12\'}','11391 2009-01-04 13:35:50Z ian']
                for j in j15:
                    rsearch = re.search(j,file_source[1])
                    if rsearch is not None:
                        cmseek.success('Joomla version detected, version: ' + cmseek.bold + '1.5' + cmseek.cln)
                        return '1.5'

                # Joomla version 1.7
                j17 = ['system.css 21322 2011-05-11 01:10:29Z dextercowley','MooTools.More={version:"1.3.2.1"','22183 2011-09-30 09:04:32Z infograf768','21660 2011-06-23 13:25:32Z infograf768']
                for j in j17:
                    rsearch = re.search(j,file_source[1])
                    if rsearch is not None:
                        cmseek.success('Joomla version detected, version: ' + cmseek.bold + '1.7' + cmseek.cln)
                        return '1.7'

            # Joomla version 1.0
            j10 = ['(Copyright (C) 2005 - 200(6|7))','47 2005-09-15 02:55:27Z rhuk','423 2005-10-09 18:23:50Z stingrey','1005 2005-11-13 17:33:59Z stingrey','1570 2005-12-29 05:53:33Z eddieajau','2368 2006-02-14 17:40:02Z stingrey','1570 2005-12-29 05:53:33Z eddieajau','4085 2006-06-21 16:03:54Z stingrey','4756 2006-08-25 16:07:11Z stingrey','5973 2006-12-11 01:26:33Z robs','5975 2006-12-11 01:26:33Z robs']
            for j in j10:
                rsearch = re.search(j,file_source[1])
                if rsearch is not None:
                    cmseek.success('Joomla version detected, version: ' + cmseek.bold + '1.0' + cmseek.cln)
                    return '1.0'

            # Joomla version 2.5
            j25 = ['Copyright (C) 2005 - 2012 Open Source Matters','MooTools.More={version:"1.4.0.1"']
            for j in j25:
                rsearch = re.search(j,file_source[1])
                if rsearch is not None:
                    cmseek.success('Joomla version detected, version: ' + cmseek.bold + '2.5' + cmseek.cln)
                    return '2.5'

    # Detection using README file
    if version == '0':
        cmseek.statement('Detecting version from README file [Method 4 of 4]')
        readme_file = url + '/README.txt'
        readme_source = cmseek.getsource(readme_file, ua)
        if readme_source[0] == '1':
            regex_4 = re.findall(r'package to version (.*?)', readme_source[1])
            if regex_4 != []:
                cmseek.success('Joomla version detected, version: ' + cmseek.bold + regex_4[0] + cmseek.cln)
                return regex_4[0]

    # if we fail ¯\_(ツ)_/¯
    return version
