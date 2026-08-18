#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

def start(id, url, ua, ga, source, ga_content, detection_method='', headers='', should_return=False, silent=False):
    if id == "wp":
        # for now this is the only cms... but not for long!
        import deepscans.wp.init as wpscan
        res = wpscan.start(id, url, ua, ga, source, detection_method, should_return=should_return, silent=silent)
    if id == 'joom':
        # told ya... not for long
        import deepscans.joom.init as joomscan
        res = joomscan.start(id, url, ua, ga, source, should_return=should_return, silent=silent)
    if id == 'umbraco':
        # umm... whatever
        import deepscans.umbraco.init as umbracoscan
        res = umbracoscan.start(id, url, ua, ga, source, detection_method, headers, should_return=should_return, silent=silent)
    if should_return:
        # Return the result for the api mode :D
        return res