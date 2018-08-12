#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 Tuhinshubhra
# This file contains all the methods of detecting cms via http Headers
# Version: 1.0.0
# Return a list with ['1'/'0','ID of CMS'/'na'] 1 = detected 0 = not detected
import re
def check(h):
    if h == "":
        return ['0', 'na']
    else:
        hstring = h
        # harray = h.split("\n") # will use whenever necessary 

        #### START DETECTION FROM HERE

        if '/wp-json/' in hstring:
            ## WordPress
            return ['1','wp']

        elif 'X-Drupal-' in hstring or '19 Nov 1978 05' in hstring:
            ## Drupal [the date is interesting isn't it? just google for it ;) ]
            return ['1', 'dru']

        elif 'Expires: Wed, 17 Aug 2005 00:00:00 GMT' in hstring:
            ## This is the only weird but common header i noticed in joomla Sites
            return ['1', 'joom']

        elif 'X-Wix-' in hstring:
            return ['1', 'wix']

        elif 'Set-Cookie: ushahidi' in hstring:
            return ['1', 'ushahidi']

        elif 'X-Generated-By: UMI.CMS' in hstring:
            return ['1', 'umi']

        elif 'x-generator: Sulu' in hstring:
            return ['1', 'sulu']

        elif 'X-Powered-CMS: Subrion CMS' in hstring:
            return ['1', 'subcms']

        elif 'Set-Cookie: SQ_SYSTEM_SESSION' in hstring or 'squizedge.net' in hstring:
            return ['1', 'sqm']

        elif 'spincms' in hstring:
            return ['1', 'spin']

        elif 'solodev_session' in hstring:
            return ['1', 'sdev']

        elif 'SC_ANALYTICS_GLOBAL_COOKIE' in hstring:
            return ['1', 'score']

        elif 'X-ServedBy: simplebo' in hstring or '_simplebo_tool_session' in hstring:
            return ['1', 'spb']

        elif 'X-Blog: Serendipity' in hstring or 'Set-Cookie: serendipity[' in hstring or 'Set-Cookie: s9y_' in hstring:
            return ['1', 'spity']

        elif 'Set-Cookie: SEAMLESS_IDENTIFIER' in hstring:
            return ['1', 'slcms']

        elif 'X-Powered-By: Roadiz CMS' in hstring:
            return ['1', 'roadz']

        elif 'X-Powered-By: pimcore' in hstring:
            return ['1', 'pcore']

        elif 'x-powered-by: PencilBlue' in hstring:
            return ['1', 'pblue']

        elif 'x-powered-by: Ophal' in hstring:
            return ['1', 'ophal']

        elif 'Server: OpenCms' in hstring:
            return ['1', 'ocms']

        elif 'X-Odoo-' in hstring:
            return ['1', 'odoo']

        elif 'X-SharePointHealthScore' in hstring or 'SPIisLatency' in hstring or 'SPRequestGuid' in hstring or 'MicrosoftSharePointTeamServices' in hstring or 'SPRequestDuration' in hstring:
            return ['1', 'share']

        elif 'october_session' in hstring:
            return ['1', 'octcms']

        elif 'Generator: Mura CMS' in hstring:
            return ['1', 'mura']

        elif 'X-Powered-By: MODX' in hstring:
            return ['1', 'modx']

        elif 'X-KoobooCMS-Version' in hstring:
            return ['1', 'kbcms']

        elif 'X-Jimdo-' in hstring:
            return ['1', 'jimdo']

        elif 'Set-Cookie: ndxz_' in hstring:
            return ['1', 'ibit']

        lep_regex = re.search(r'lep(.*?)sessionid', hstring)
        if lep_regex != None:
            return ['1', 'lepton']

        else:
            return ['0', 'na']
