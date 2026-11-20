#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2023 hackzard

# Detect cms using directory (modules) checks
# Rev 1
import re
import cmseekdb.basic as cmseek
def check(url, ua):
    directories = ["/manager/", "/admin/", "/about/"]
    # check for modules directory
    for directory in directories:
            directory = url.rstrip('/') + directory
            page_source = cmseek.getsource(directory, ua)
            if page_source[0] == '1' and page_source[1] != '':
                # Check begins here
                page_content = page_source[1]
                #### START DETECTION FROM HERE
                ## || <- if either of it matches cms detected
                ## :::: <- all the strings has to match (implemented to decrease false positives)
                directory_detection_keys = [
                'http://modx.com||MODX CMF Manager Login||/MODxRE/:-modx',
                'SilverStripe:-sst',
                'bitrix||Bitrix:-bitrix'
                ]
                for detection_key in directory_detection_keys:
                    if ':-' in detection_key:
                        detection_array = detection_key.split(':-')
                        if '||' in detection_array[0]:
                            detection_strings = detection_array[0].split('||')
                            for detection_string in detection_strings:
                                if detection_string in page_content and detection_array[1] not in cmseek.ignore_cms:
                                    if cmseek.strict_cms == [] or detection_array[1] in cmseek.strict_cms:
                                        return ['1', detection_array[1]]
                        elif '::::' in detection_array[0]:
                            match_status = '0' # 0 = neutral, 1 = passed, 2 = failed
                            match_strings = detection_array[0].split('::::')
                            for match_string in match_strings:
                                if match_status == '0' or match_status == '1':
                                    if match_string in page_content:
                                        match_status = '1'
                                    else:
                                        match_status = '2'
                                else:
                                    match_status = '2'
                            if match_status == '1' and detection_array[1] not in cmseek.ignore_cms:
                                if cmseek.strict_cms == [] or detection_array[1] in cmseek.strict_cms:
                                    return ['1', detection_array[1]]
                        else:
                            if detection_array[0] in page_content and detection_array[1] not in cmseek.ignore_cms:
                                if cmseek.strict_cms == [] or detection_array[1] in cmseek.strict_cms:
                                    return ['1', detection_array[1]]
    else:
        cmseek.error('Unable to detect CMS even by directory (modules) checks!')
        return ['0','']
