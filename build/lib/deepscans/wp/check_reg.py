#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

# http://localhost/wordpress/wordpress/wp-login.php?action=register

import cmseekdb.basic as cmseek

def start(url,ua):
    reg_url = url + '/wp-login.php?action=register'
    cmseek.info('Checking user registration status')
    reg_source = cmseek.getsource(reg_url, ua)
    reg_status = '0'
    if reg_source[0] == '1' and '<form' in reg_source[1]:
        if 'Registration confirmation will be emailed to you' in reg_source[1] or 'value="Register"' in reg_source[1] or 'id="user_email"' in reg_source[1]:
            cmseek.success('User registration open: ' + cmseek.bold + cmseek.fgreen + reg_url + cmseek.cln)
            reg_status = '1'
    return [reg_status, reg_url]
