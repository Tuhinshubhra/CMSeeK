#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

import threading
import cmseekdb.basic as cmseek

joom_dir_found = 0
joom_dirs = []

def check_directory(url,file,ua):
    global joom_dir_found, joom_dirs
    file_check = cmseek.getsource(url + '/' + file, ua)
    if file_check[0] == '1':
        if 'Index of' in file_check[1] or 'Last modified</a>' in file_check[1]:
            cmseek.success('Directory listing enabled in: ' + cmseek.bold + cmseek.fgreen + file + cmseek.cln)
            joom_dir_found += 1
            joom_dirs.append(file)

def start(url, ua):
    directory_files = ['administrator/components','components','administrator/modules','modules','administrator/templates','templates','cache','images','includes','language','media','templates','tmp','images/stories','images/banners']
    threads = [threading.Thread(target=check_directory, args=(url, file ,ua)) for file in directory_files]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    global joom_dir_found, joom_dirs
    return [joom_dir_found, joom_dirs]
