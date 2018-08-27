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

        elif 'X-Jcms-Ajax-Id' in hstring:
            return ['1', 'jcms']

        elif 'Set-Cookie: grav-site-' in hstring:
            return ['1', 'grav']

        elif 'X-Powered-By: FlexCMP' in hstring or 'X-Flex-Tag:' in hstring or 'X-Flex-Lang:' in hstring or 'X-Flex-Lastmod:' in hstring or 'X-Flex-Community:' in hstring or 'X-Flex-Evstart' in hstring:
            return ['1', 'flex']

        elif 'X-Powered-By: eZ Publish' in hstring or 'Set-Cookie: eZSESSID' in hstring:
            return ['1', 'ezpu']

        elif 'Set-Cookie: exp_tracker' in hstring or 'Set-Cookie: exp_last_activity' in hstring or 'Set-Cookie: exp_last_visit' in hstring or 'Set-Cookie: exp_csrf_token=' in hstring:
            return ['1', 'exen']

        elif 'X-Powered-By: e107' in hstring or 'Set-Cookie: SESSE107COOKIE' in hstring:
            return ['1', 'e107']

        elif 'Set-Cookie: dnn_IsMobile' in hstring or 'DNNOutputCache' in hstring or 'DotNetNuke' in hstring:
            return ['1', 'dnn']

        elif 'X-Powered-By: CMS Danneo' in hstring:
            return ['1', 'dncms']

        elif 'X-Powered-By: Craft CMS' in hstring or 'Set-Cookie: CraftSessionId' in hstring:
            return ['1', 'craft']

        elif 'X-Powered-By: Dragonfly CMS' in hstring:
            return ['1', 'dragon']

        elif 'X-Generator: Orchard' in hstring:
            return ['1', 'orchd']

        elif 'X-Powered-By: ContentBox' in hstring or 'Set-Cookie: LIGHTBOXSESSION' in hstring:
            return ['1', 'cbox']

        elif 'Set-Cookie: CONCRETE5' in hstring:
            return ['1', 'con5']

        elif 'X-Discourse-Route' in hstring:
            return ['1', 'dscrs']

        elif 'Set-Cookie: flarum_session=' in hstring:
            return ['1', 'flarum']

        elif 'IPSSessionFront' in hstring or 'ipbWWLmodpids' in hstring or 'ipbWWLsession_id' in hstring:
            return ['1', 'ipb']

        elif 'X-Powered-By: NodeBB' in hstring:
            return ['1', 'nodebb']

        elif 'X-Garden-Version: Vanilla' in hstring or 'Maybe you should be reading this instead: https://www.vanillaforums.com/en/careers' in hstring:
            return ['1', 'vanilla']

        elif 'Set-Cookie: xf_session=' in hstring or 'Set-Cookie: xf_csrf=' in hstring:
            return ['1', 'xf']

        elif '[aefsid]' in hstring:
            return ['1', 'aef']

        elif 'Set-Cookie: fud_session_' in hstring:
            return ['1', 'fudf']

        elif 'Set-Cookie: phorum_session' in hstring:
            return ['1', 'phorum']

        elif 'Set-Cookie: yazdLastVisited=' in hstring:
            return ['1', 'yazd']

        elif 'Set-Cookie: ubbt_' in hstring:
            return ['1', 'ubbt']


        ####################################################
        #         REGEX DETECTIONS STARTS FROM HERE        #
        ####################################################

        ybb_regex = re.search(r'Set-Cookie: (YaBBusername=|YaBBpassword=|YaBBSession|Y2User-(\d.*?)|Y2Pass-(\d.*?)|Y2Sess-(\d.*?))=', hstring)
        if ybb_regex != None:
            return ['1', 'yabb']

        xmb_regex = re.search(r'Set-Cookie: xmblv(a|b)=(\d.*?)\n',hstring)
        if xmb_regex != None:
            return ['1', 'xmb']

        wind_regex = re.search(r'Set-Cookie: [a-zA-Z0-9]{5}_(lastpos|lastvisit)=', hstring)
        if wind_regex != None:
            return ['1', 'pwind']

        myb_regex = re.search(r'Set-Cookie: mybb\[(.*?)\]=', hstring)
        if myb_regex != None:
            return ['1', 'mybb']

        bb_regex = re.search(r'Set-Cookie: wcf(.*?)_cookieHash=', hstring)
        if bb_regex != None:
            return ['1', 'bboard']

        epis_regex = re.search(r'X-XRDS-Location: (.*?)EPiServerCommunity', hstring)
        if epis_regex != None:
            return ['1', 'epis']

        lep_regex = re.search(r'lep(.*?)sessionid', hstring)
        if lep_regex != None:
            return ['1', 'lepton']

        pb_regex = re.search(r'Set-Cookie: phpbb(.*?)=', hstring)
        if pb_regex != None:
            return ['1', 'phpbb']

        ses_regex = re.search(r'Set-Cookie: ses(\d+)=', hstring)
        if ses_regex != None:
            return ['1', 'impage']

        else:
            return ['0', 'na']
