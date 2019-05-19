#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2019 Tuhinshubhra
# This file contains all the methods of detecting cms via http Headers
# Version: 1.0.0
# Return a list with ['1'/'0','ID of CMS'/'na'] 1 = detected 0 = not detected
import re
import cmseekdb.basic as cmseek

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
        'Set-Cookie: bigwareCsid||Set-Cookie: bigWAdminID:-bigw',
        'X-ATG-Version:-oracle_atg',
        'Set-Cookie: MoodleSession||Set-Cookie: MOODLEID_:-mdle',
        'COMMERCE-SERVER-SOFTWARE:||commerce-server-software::-coms',
        'Set-Cookie: COSMOSHOP_:-cosmos',
        'Set-Cookie: Dynamicweb:-dweb',
        'X-Elcodi::-elcd',
        'X-Powered-By: eZ Publish:-ezpub',
        'Powered-By: PrestaShop||Set-Cookie: PrestaShop:-presta',
        'Demandware Secure Token||Demandware anonymous cookie||dwpersonalization_||dwanonymous_:-sfcc',
        'X-Umbraco-Version:-umbraco',
        'X-Shopery||This E-commerce is built using Shopery:-shopery',
        'X-Powered-By: ShopFA:-shopfa',
        'X-ShopId::::X-ShardId:-shopify',
        'X-Shopify-Stage||set-cookie: _shopify||Set-Cookie: secure_customer_sig:-shopify',
        'SRV_ID=shoptet:-shoptet'
        ]        
        for keyl in hkeys:
            if ':-' in keyl:
                det = keyl.split(':-')
                if '||' in det[0]:
                    idkwhat = det[0]
                    dets = idkwhat.split('||')
                    for d in dets:
                        if d in hstring and det[1] not in cmseek.ignore_cms: # ignore cms thingy
                            if cmseek.strict_cms == [] or det[1] in cmseek.strict_cms:
                                return ['1', det[1]]
                elif '::::' in det[0]:
                    # yet again i know there can be a better way of doing it and feel free to correct it :)
                    and_chk = '0' # 0 = neutral, 1 = passed, 2 = failed
                    chks = det[0].split('::::')
                    for chk in chks:
                        if and_chk == '0' or and_chk == '1':
                            if chk in hstring:
                                and_chk = '1'
                            else:
                                and_chk = '2'
                        else:
                            and_chk = '2'
                    if and_chk == '1' and det[1] not in cmseek.ignore_cms:
                        if cmseek.strict_cms == [] or det[1] in cmseek.strict_cms:
                            return ['1', det[1]]
                else:
                    if det[0] in hstring and det[1] not in cmseek.ignore_cms:
                        if cmseek.strict_cms == [] or det[1] in cmseek.strict_cms:
                            return ['1', det[1]]

        ####################################################
        #         REGEX DETECTIONS STARTS FROM HERE        #
        ####################################################

        rgxkeys = [
        'Set-Cookie: (YaBBusername=|YaBBpassword=|YaBBSession|Y2User-(\d.*?)|Y2Pass-(\d.*?)|Y2Sess-(\d.*?))=:-yabb',
        'Set-Cookie: xmblv(a|b)=(\d.*?)\n:-xmb',
        'Set-Cookie: [a-zA-Z0-9]{5}_(lastpos|lastvisit)=:-pwind',
        'Set-Cookie: mybb\[(.*?)\]=:-mybb',
        'Set-Cookie: wcf(.*?)_cookieHash=:-bboard',
        'X-XRDS-Location: (.*?)EPiServerCommunity:-epis',
        'lep(.*?)sessionid:-lepton',
        'Set-Cookie: phpbb(.*?)=:-phpbb',
        'Set-Cookie: ses(\d+)=:-impage',
        'Set-Cookie: sid_customer_[a-zA-Z0-9]{5}=:-csc'
        ]
        # so here's the story, i've been watching hunter x hunter for last 2 weeks and i just finished it.
        # In the following lines you'll find some weird variable names, those are characters from hxh.
        # Thank you for reading this utterly useless comment.. now let's get back to work!
        for hxh in rgxkeys:
            if ':-' in hxh:
                hunter = hxh.split(':-')
                if '||' in hunter[0]:
                    gon = hunter[0].split('||')
                    for killua in gon:
                        natero = re.search(killua, hstring, re.DOTALL)
                        if natero != None and hunter[1] not in cmseek.ignore_cms:
                            if cmseek.strict_cms == [] or hunter[1] in cmseek.strict_cms:
                                return ['1', hunter[1]]
                else:
                    natero = re.search(hunter[0], hstring, re.DOTALL)
                    if natero != None and hunter[1] not in cmseek.ignore_cms:
                        if cmseek.strict_cms == [] or det[1] in cmseek.strict_cms:
                            return ['1', hunter[1]]
        else:
            # Failure
            return ['0', 'na']
