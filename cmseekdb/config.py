#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 Tuhinshubhra

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
    cmseek_version = '1.1.0' # Failsafe measure i guess

# well the log containing variable
log = '{"url":"","last_scanned":"","detection_param":"","cms_id":"","cms_name":"","cms_url":""}'
log_dir = ""
