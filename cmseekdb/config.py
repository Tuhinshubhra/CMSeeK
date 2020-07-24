#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

# Verbose
verbose = False

# GitHub repo link
GIT_URL = 'https://github.com/Tuhinshubhra/CMSeeK'

# Version thingy
try:
    rv = open('current_version', 'r')
    cver = rv.read().replace('\n','')
    cmseek_version = cver
except:
    cmseek_version = '1.1.3' # Failsafe measure i guess

# well the log containing variable, no need to edit anything here
log = '{"url":"","last_scanned":"","detection_param":"","cms_id":"","cms_name":"","cms_url":""}'
log_dir = ""

# access_directory contains the path to the directory where reports directory and reports.json files are saved
# leave it empty to use default dir (cmseek directory if writeaccess else the current directory the user is in)
# if you want to use a custom path.. enter the full path below

access_directory = ""