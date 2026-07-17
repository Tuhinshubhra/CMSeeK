#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

import cmseekdb.basic as cmseek

def start(url,ua):
    reg_url = url + '/index.php?option=com_users&view=registration'
    reg_source = cmseek.getsource(reg_url, ua)
    if reg_source[0] == '1':
        if 'registration.register' in reg_source[1] or 'jform_password2' in reg_source[1] or 'jform_email2' in reg_source[1]:
            cmseek.success('User registration open, ' + cmseek.bold + reg_url + cmseek.cln)
            return ['1', reg_url]
        else:
            return ['0', '']
    else:
        return ['0', '']
