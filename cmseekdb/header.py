#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra
# This file contains all the methods of detecting cms via http Headers
# Version: 1.0.0
# Return a list with ['1'/'0','ID of CMS'/'na'] 1 = detected 0 = not detected
import re
import cmseekdb.basic as cmseek

def check(hstring):
    if hstring == "":
        return ['0', 'na']
    else:
        #hstring = h
        # harray = h.split("\n") # will use whenever necessary

        #### START DETECTION FROM HERE

        header_detection_keys = [
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
        'SRV_ID=shoptet:-shoptet',
        'Set-Cookie: _SOLUSQUARE:-solusquare',
        'Set-Cookie: _spree_store_session:-spree',
        'X-Powered-CMS: Bitrix Site Manager:-bitrix',
        'X-Powered-By: Brightspot:-brightspot',
        'Set-Cookie: WHMCS:-whmcs',
        'X-Powered-By: OpenNemas||Via: Opennemas Proxy Server:-opennemas'
        ]        
        for header_key in header_detection_keys:
            if ':-' in header_key:
                detection_string = header_key.split(':-')
                if '||' in detection_string[0]:
                    # check if there are multiple detection strings
                    detection_strings = detection_string[0].split('||')
                    for d in detection_strings:
                        if d in hstring and detection_string[1] not in cmseek.ignore_cms: # ignore cms thingy - what i mean is check if the cms_id is not in the ignore list
                            if cmseek.strict_cms == [] or detection_string[1] in cmseek.strict_cms:
                                return ['1', detection_string[1]]
                elif '::::' in detection_string[0]:
                    # :::: is used when we want to check if both detection strings are present in the header. 
                    match_status = '0' # 0 = neutral, 1 = passed, 2 = failed
                    keys_to_match = detection_string[0].split('::::')
                    for check_key in keys_to_match:
                        if match_status == '0' or match_status == '1':
                            if check_key in hstring:
                                match_status = '1'
                            else:
                                match_status = '2'
                        else:
                            match_status = '2'
                    if match_status == '1' and detection_string[1] not in cmseek.ignore_cms:
                        if cmseek.strict_cms == [] or detection_string[1] in cmseek.strict_cms:
                            return ['1', detection_string[1]]
                else:
                    if detection_string[0] in hstring and detection_string[1] not in cmseek.ignore_cms:
                        if cmseek.strict_cms == [] or detection_string[1] in cmseek.strict_cms:
                            return ['1', detection_string[1]]

        ####################################################
        #         REGEX DETECTIONS STARTS FROM HERE        #
        ####################################################

        header_detection_keys_regex = [
        'Set-Cookie: (YaBBusername=|YaBBpassword=|YaBBSession|Y2User-(\d.*?)|Y2Pass-(\d.*?)|Y2Sess-(\d.*?))=:-yabb',
        'Set-Cookie: xmblv(a|b)=(\d.*?)\n:-xmb',
        'Set-Cookie: [a-zA-Z0-9]{5}_(lastpos|lastvisit)=:-pwind',
        'Set-Cookie: mybb\[(.*?)\]=:-mybb',
        'Set-Cookie: wcf(.*?)_cookieHash=:-bboard',
        'X-XRDS-Location: (.*?)EPiServerCommunity:-epis',
        'lep(.*?)sessionid:-lepton',
        'Set-Cookie: phpbb(.*?)=:-phpbb',
        'Set-Cookie: ses(\d+)=:-impage',
        'Set-Cookie: sid_customer_[a-zA-Z0-9]{5}=:-csc',
        'X-Host: (.*?)weebly.net:-weebly',
        'Set-Cookie: (ekmMsg|ekmpowershop):-ekmps'
        ]
        # so here's the story, i've been watching regex_key x regex_key for last 2 weeks and i just finished it.
        # In the following lines you'll find some weird variable names, those are characters from detection_key.
        # Thank you for reading this utterly useless comment.. now let's get back to work!

        # Update 2019 - ^ That was a mistake time to fix this abomination
        for detection_key in header_detection_keys_regex:
            if ':-' in detection_key:
                regex_key = detection_key.split(':-')
                if '||' in regex_key[0]:
                    match_strings = regex_key[0].split('||')
                    for match_string in match_strings:
                        regex_match_status = re.search(match_string, hstring, re.DOTALL)
                        if regex_match_status != None and regex_key[1] not in cmseek.ignore_cms:
                            if cmseek.strict_cms == [] or regex_key[1] in cmseek.strict_cms:
                                return ['1', regex_key[1]]
                else:
                    regex_match_status = re.search(regex_key[0], hstring, re.DOTALL)
                    if regex_match_status != None and regex_key[1] not in cmseek.ignore_cms:
                        if cmseek.strict_cms == [] or regex_key[1] in cmseek.strict_cms:
                            return ['1', regex_key[1]]
        else:
            # Failure
            return ['0', 'na']
