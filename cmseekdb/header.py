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

        hkeys = [
        '/wp-json/:-wp',
        'X-Drupal-||19 Nov 1978 05:-dru',
        'Expires: Wed, 17 Aug 2005 00:00:00 GMT:-joom',
        'X-Wix-:-wix',
        'Set-Cookie: ushahidi:-ushahidi',
        'X-Generated-By: UMI.CMS:-umi',
        'x-generator: Sulu:-sulu',
        'X-Powered-CMS: Subrion CMS:-subcms',
        'Set-Cookie: SQ_SYSTEM_SESSION||squizedge.net:-sqm',
        'spincms:-spin',
        'solodev_session:-sdev',
        'SC_ANALYTICS_GLOBAL_COOKIE:-score',
        'X-ServedBy: simplebo||_simplebo_tool_session:-spb',
        'X-Blog: Serendipity||Set-Cookie: serendipity[||Set-Cookie: s9y_:-spity',
        'Set-Cookie: SEAMLESS_IDENTIFIER:-slcms',
        'X-Powered-By: Roadiz CMS:-roadz',
        'X-Powered-By: pimcore:-pcore',
        'x-powered-by: PencilBlue:-pblue',
        'x-powered-by: Ophal:-ophal',
        'Server: OpenCms:-ocms',
        'X-Odoo-:-odoo',
        'X-SharePointHealthScore||SPIisLatency||SPRequestGuid||MicrosoftSharePointTeamServices||SPRequestDuration:-share',
        'october_session:-octcms',
        'Generator: Mura CMS:-mura',
        'X-Powered-By: MODX:-modx',
        'X-KoobooCMS-Version:-kbcms',
        'X-Jimdo-:-jimdo',
        'Set-Cookie: ndxz_:-ibit',
        'X-Jcms-Ajax-Id:-jcms',
        'Set-Cookie: grav-site-:-grav',
        'X-Powered-By: FlexCMP||X-Flex-Tag:||X-Flex-Lang:||X-Flex-Lastmod:||X-Flex-Community:||X-Flex-Evstart:-flex',
        'X-Powered-By: eZ Publish||Set-Cookie: eZSESSID:-ezpu',
        'Set-Cookie: exp_tracker||Set-Cookie: exp_last_activity||Set-Cookie: exp_last_visit||Set-Cookie: exp_csrf_token=:-exen',
        'X-Powered-By: e107||Set-Cookie: SESSE107COOKIE:-e107',
        'Set-Cookie: dnn_IsMobile||DNNOutputCache||DotNetNuke:-dnn',
        'X-Powered-By: CMS Danneo:-dncms',
        'X-Powered-By: Craft CMS||Set-Cookie: CraftSessionId:-craft',
        'X-Powered-By: Dragonfly CMS:-dragon',
        'X-Generator: Orchard:-orchd',
        'X-Powered-By: ContentBox||Set-Cookie: LIGHTBOXSESSION:-cbox',
        'Set-Cookie: CONCRETE5:-con5',
        'X-Discourse-Route:-dscrs',
        'Set-Cookie: flarum_session=:-flarum',
        'IPSSessionFront||ipbWWLmodpids||ipbWWLsession_id:-ipb',
        'X-Powered-By: NodeBB:-nodebb',
        'X-Garden-Version: Vanilla||Maybe you should be reading this instead: https://www.vanillaforums.com/en/careers:-vanilla',
        'Set-Cookie: xf_session=||Set-Cookie: xf_csrf=:-xf',
        '[aefsid]:-aef',
        'Set-Cookie: fud_session_:-fudf',
        'Set-Cookie: phorum_session:-phorum',
        'Set-Cookie: yazdLastVisited=:-yazd',
        'Set-Cookie: ubbt_:-ubbt',
        'X-Powered-By: Afosto||Link: <//afosto-cdn:-afsto',
        'X-Arastta:-arstta',
        'set-cookie: fornax_anonymousId=:-bigc',
        'Set-Cookie: bigwareCsid||Set-Cookie: bigWAdminID:-bigw'
        ]
        for keyl in hkeys:
            if ':-' in keyl:
                det = keyl.split(':-')
                if '||' in det[0]:
                    idkwhat = det[0]
                    dets = idkwhat.split('||')
                    for d in dets:
                        if d in hstring:
                            return ['1', det[1]]
                else:
                    if det[0] in hstring:
                        return ['1', det[1]]

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
