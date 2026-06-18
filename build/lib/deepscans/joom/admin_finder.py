#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

import threading
import cmseekdb.basic as cmseek

joom_admin_found = 0
joom_admins = []

def check_admin(url,file,ua):
    global joom_admin_found, joom_admins
    file_check = cmseek.check_url(url + '/' + file, ua)
    if file_check == '1':
        cmseek.success('Admin login page found: ' + cmseek.bold + cmseek.fgreen + url + '/' + file + cmseek.cln)
        joom_admin_found += 1
        joom_admins.append(file)

def start(url, ua):
    admin_files = ['administrator','admin','panel','webadmin','modir','manage','administration','joomla/administrator','joomla/admin']
    threads = [threading.Thread(target=check_admin, args=(url, file ,ua)) for file in admin_files]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    global joom_admin_found, joom_admins
    return [joom_admin_found, joom_admins]
