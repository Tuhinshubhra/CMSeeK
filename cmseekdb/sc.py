#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 Tuhinshubhra

# This file contains all the methods of detecting cms via Source Code
# Version: 1.0.0
# Return a list with ['1'/'0','ID of CMS'/'na'] 1 = detected 0 = not detected 2 = No Sourcecode Provided

import re

def check(s, site): ## Check if no generator meta tag available
    if s == "": ## No source code provided kinda shitty check but oh well
        return ['2', 'na']
    else: ## The real shit begins here
        hstring = s
        # harray = s.split("\n") ### Array conversion can use if needed later
        if '/wp-content/' in hstring:
            # WordPress
            return ['1','wp']

        elif '/skin/frontend/' in hstring:
            # Magento
            return ['1','mg']

        elif 'https://www.blogger.com/static/' in hstring:
            # Blogger By Google
            return ['1','blg']

        elif 'ic.pics.livejournal.com' in hstring:
            # LiveJournal
            return ['1','lj']

        elif 'END: 3dcart stats' in hstring:
            # 3D Cart
            return ['1','tdc']

        elif 'href="/apos-minified/' in hstring:
            # Apostrophe CMS
            return ['1','apos']

        # elif 'WebFontConfig = ' in hstring:
        #    # Bubble CMS
        #    return ['1','bubble']

        elif 'href="/CatalystStyles/' in hstring:
            # Adobe Business Catalyst
            return ['1','abc']

        elif 'src="/misc/drupal.js"' in hstring:
            # Drupal
            return ['1', 'dru']

        elif 'css/joomla.css' in hstring: # Lamest one possible
             # Obvious Joomla
             return ['1','joom']

        elif 'Powered By <a href="http://www.opencart.com">OpenCart' in hstring or "catalog/view/javascript/jquery/swiper/css/opencart.css" in hstring or 'index.php?route=' in hstring:
            # OpenCart
            return ['1', 'oc']

        elif '/xoops.js' in hstring or 'xoops_redirect' in hstring:
            # XOOPS
            return ['1', 'xoops']

        elif 'Wolf Default RSS Feed' in hstring:
            # Wolf CMS
            return ['1', 'wolf']

        elif '/ushahidi.js' in hstring or 'alt="Ushahidi"' in hstring:
            # ushahidi (weird freaking name)
            return ['1', 'ushahidi']

        elif 'getWebguiProperty' in hstring:
            # WebGUI
            return ['1', 'wgui']

        elif 'title: "TiddlyWiki"' in hstring or 'TiddlyWiki created by Jeremy Ruston,' in hstring:
            # Tiddly Wiki
            return ['1','tidw']

        elif 'Running Squiz Matrix' in hstring:
            # Squiz Matrix
            return ['1', 'sqm']

        elif 'assets.spin-cdn.com' in hstring:
            # Spin CMS
            return ['1', 'spin']

        elif 'content="Solodev" name="author"' in hstring:
            # solodev
            return ['1', 'sdev']

        elif 'content="sNews' in hstring:
            # sNews
            return ['1', 'snews']

        elif '/api/sitecore/' in hstring:
            # sitecore
            return ['1', 'score']

        elif 'simsite/' in hstring:
            # SIMsite
            return ['1', 'sim']

        elif 'simplebo.net/' in hstring  or '"pswp__' in hstring:
            # Simplebo
            return ['1', 'spb']

        elif '/silvatheme' in hstring:
            # Silva CMS
            return ['1', 'silva']

        elif 'serendipityQuickSearchTermField' in hstring  or '"serendipity_' in hstring or 'serendipity[' in hstring:
            # Serendipity
            return ['1', 'spity']

        elif 'Published by Seamless.CMS.WebUI' in hstring:
            # SeamlessCMS
            return ['1', 'slcms']

        elif 'rock-config-trigger' in hstring or 'rock-config-cancel-trigger' in hstring:
            # RockRMS
            return ['1', 'rock']

        elif '/rcms-f-production.' in hstring:
            # RCMS
            return ['1', 'rcms']

        elif 'CMS by Quick.Cms' in hstring or 'read license: www.opensolution.org/license.html' in hstring:
            # Quick.Cms
            return ['1', 'quick']

        elif '"pimcore_' in hstring:
            # Pimcore
            return ['1', 'pcore']

        elif 'xmlns:perc' in hstring or 'cm/css/perc_decoration.css' in hstring:
            # Percussion CMS
            return ['1', 'percms']

        elif 'PencilBlueController' in hstring or '"pencilblueApp"' in hstring:
            # PencilBlue
            return ['1', 'pblue']

        elif '/libraries/ophal.js' in hstring:
            # Ophal
            return ['1', 'ophal']

        elif 'Sitefinity/WebsiteTemplates' in hstring:
            # Sitefinity
            return ['1', 'sfy']

        elif 'published by Open Text Web Solutions' in hstring:
            # OpenText WSM
            return ['1', 'otwsm']

        elif '/opencms/export/' in hstring:
            # OpenCms
            return ['1', 'ocms']

        elif 'odoo.session_info' in hstring or 'var odoo =' in hstring:
            # Odoo
            return ['1', 'odoo']

        elif '_spBodyOnLoadWrapper' in hstring or '_spPageContextInfo' in hstring or '_spFormOnSubmitWrapper' in hstring:
            # Microsoft SharePoint
            return ['1', 'share']

        elif '/storage/app/media/' in hstring:
            # October CMS
            return ['1', 'octcms']

        elif 'mura.min.css' in hstring or '/plugins/Mura' in hstring:
            # Mura CMS
            return ['1', 'mura']

        elif 'mt-content/' in hstring or 'moto-website-style' in hstring:
            # Moto CMS
            return ['1', 'moto']

        elif 'mono_donottrack' in hstring or 'monotracker.js' in hstring  or '_monoTracker' in hstring:
            # Mono.net
            return ['1', 'mnet']

        elif 'Powered by MODX</a>' in hstring:
            # MODX
            return ['1', 'modx']

        elif "siteCMS:'methode'" in hstring or "contentOriginatingCMS='Methode'" in hstring or 'Methode tags version' in hstring or '/r/PortalConfig/common/assets/' in hstring:
            # Methode
            return ['1', 'methd']

        elif 'var LIVESTREET_SECURITY_KEY' in hstring:
            # LiveStreet CMS
            return ['1', 'lscms']

        elif '/koken.js' in hstring or 'data-koken-internal' in hstring:
            # Koken
            return ['1', 'koken']

        elif 'jimdo_layout_css' in hstring or 'var jimdoData' in hstring or 'isJimdoMobileApp' in hstring:
            # Jimdo
            return ['1', 'jimdo']

        elif '<!-- you must provide a link to Indexhibit' in hstring or "Built with <a href='http://www.indexhibit.org/'>Indexhibit" in hstring or 'ndxz-studio/site' in hstring or 'ndxzsite/' in hstring:
            # IndexHibit
            return ['1', 'ibit']

        elif '<!-- webflow css -->' in hstring or 'css/webflow.css' in hstring or 'js/webflow.js' in hstring:
            # Webflow CMS
            return ['1', 'wflow']

        elif 'css/jalios/core/' in hstring or 'js/jalios/core/' in hstring or 'jalios:ready' in hstring:
            # jalios JCMS
            return ['1', 'jcms']

        elif 'ip_themes/' in hstring or 'ip_libs/' in hstring or 'ip_cms/' in hstring:
            # ImpressPages CMS
            return ['1', 'impage']

        elif '/css_js_cache/hotaru_css' in hstring or 'hotaruFooterImg' in hstring or '/css_js_cache/hotaru_js' in hstring:
            # Hotaru CMS
            return ['1', 'hotaru']

        elif 'binaries/content/gallery/' in hstring:
            # Hippo CMS
            return ['1', 'hippo']

        elif 'PHP-Nuke Copyright ©' in hstring or 'PHP-Nuke theme by' in hstring:
            # PHP Nuke
            return ['1', 'phpn']

        elif 'FlexCMP - CMS per Siti Accessibili' in hstring or '/flex/TemplatesUSR/' in hstring or 'FlexCMP - Digital Experience Platform (DXP)' in hstring:
            # FlexCMP
            return ['1', 'flex']

        elif 'copyright" content="eZ Systems"' in hstring or 'ezcontentnavigationpart' in hstring or 'ezinfo/copyright' in hstring:
            # eZ Publish
            return ['1', 'ezpu']

        elif 'e107_files/e107.js' in hstring or 'e107_themes/' in hstring or 'e107_plugins/' in hstring:
            # e107
            return ['1', 'e107']

        elif '<!-- DNN Platform' in hstring or ' by DNN Corporation -->' in hstring or 'DNNROBOTS' in hstring or 'js/dnncore.js?' in hstring or 'dnn_ContentPane' in hstring or 'js/dnn.js?' in hstring:
            # DNN Platform
            return['1', 'dnn']

        elif 'phpBBstyle' in hstring or 'phpBBMobileStyle' in hstring or 'style_cookie_settings' in hstring:
            # phpBB
            return ['1', 'phpbb']

        elif 'dede_fields' in hstring or 'dede_fieldshash' in hstring or 'DedeAjax' in hstring or 'DedeXHTTP' in hstring or 'include/dedeajax2.js' in hstring or 'css/dedecms.css' in hstring:
            # DEDE CMS
            return ['1', 'dede']

        elif '/Orchard.jQuery/' in hstring or 'orchard.themes' in hstring or 'orchard-layouts-root' in hstring:
            # Orchard CMS
            return ['1', 'orchd']

        elif 'modules/contentbox/themes/' in hstring:
            # ContentBox
            return ['1', 'cbox']

        elif 'data-contentful' in hstring or '.contentful.com/' in hstring or '.ctfassets.net/' in hstring:
            # Contentful
            return ['1', 'conful']

        elif 'Contensis.current' in hstring or 'ContensisSubmitFromTextbox' in hstring or 'ContensisTextOnly' in hstring:
            # Contensis
            return ['1', 'contensis']

        elif 'system/cron/cron.txt' in hstring:
            # Contao
            return ['1', 'contao']

        elif '/burningBoard.css' in hstring or 'wcf/style/' in hstring:
            # Burning Board
            return ['1', 'bboard']

        elif '/concrete/images' in hstring or '/concrete/css' in hstring or '/concrete/js' in hstring:
            # Concrete5 CMS
            return ['1', 'con5']

        elif 'discourse_theme_id' in hstring or 'discourse_current_homepage' in hstring:
            # Discourse
            return ['1', 'discrs']

        elif 'discuz_uid' in hstring or 'discuz_tips' in hstring or 'content="Discuz! Team and Comsenz UI Team"' in hstring:
            # Discuz!
            return ['1', 'discuz']

        elif 'flarum-loading' in hstring or 'flarum/app' in hstring:
            # Flarum
            return ['1', 'flarum']

        elif '/* IP.Board' in hstring or 'js/ipb.js' in hstring or 'js/ipb.lang.js' in hstring:
            # IP Board
            return ['1', 'ipb']

        elif 'ips_username' in hstring and 'ips_password' in hstring:
            # IP Board
            return ['1', 'ipb']

        elif 'bb_default_style.css' in hstring or 'name="URL" content="http://www.minibb.net/"' in hstring:
            # miniBB
            return ['1', 'minibb']

        elif 'var MyBBEditor' in hstring:
            # MyBB
            return ['1', 'mybb']

        elif '/assets/nodebb.min.js' in hstring or '/plugins/nodebb-' in hstring:
            # NodeBB
            return ['1', 'nodebb']

        elif 'PUNBB.env' in hstring or 'typeof PUNBB ===' in hstring:
            # PunBB
            return ['1', 'punbb']

        elif 'Powered by SMF' in hstring:
            # SMF
            return ['1', 'smf']

        elif 'vanilla_discussions_index' in hstring or 'vanilla_categories_index' in hstring:
            # Vanilla
            return ['1', 'vanilla']

        elif 'Forum software by XenForo&trade;' in hstring or '<html id="XenForo"' in hstring or 'css.php?css=xenforo' in hstring:
            # XenForo
            return ['1', 'xf']

        elif '<!-- Powered by XMB' in hstring or '<!-- The XMB Group -->' in hstring or 'Powered by XMB' in hstring:
            # XMB
            return ['1', 'xmb']

        elif 'yabbfiles/' in hstring:
            # YaBB
            return ['1', 'yabb']

        elif 'Powered By AEF' in hstring:
            # Advanced Electron Forum
            return ['1', 'aef']

        elif 'Powered by: FUDforum' in hstring:
            # FUDforum
            return ['1', 'fudf']

        elif '<div id="phorum">' in hstring:
            # Phorum
            return ['1', 'phorum']

        elif '"YafHead' in hstring:
            # Yet Another Forum
            return ['1', 'yaf']

        elif '<!-- NoNonsense Forum' in hstring:
            # NoNonsense Forum
            return ['1', 'nnf']

        elif '/mvnplugin/mvnforum/' in hstring:
            # mvnForum
            return ['1', 'mvnf']

        elif 'aspnetforum.css"' in hstring or '_AspNetForumContentPlaceHolder' in hstring:
            # AspNetForum
            return ['1', 'aspf']

        elif 'jforum/templates/' in hstring:
            # JForum
            return ['1', 'jf']

        ####################################################
        #         REGEX DETECTIONS STARTS FROM HERE        #
        ####################################################

        jf_regex = re.search(r'Powered by(.*?)JForum(.*?)</a>', hstring)
        if jf_regex != None:
            # JForum
            return ['1', 'jf']

        aspf_regex = re.search(r'Powered by(.*?)AspNetForum(.*?)(</a>|</span>)', hstring)
        if aspf_regex != None:
            # AspNetForum
            return ['1', 'aspf']

        mcb_regex = re.search(r'Powered by(.*?)MercuryBoard(.*?)</a>', hstring)
        if mcb_regex != None:
            # MercuryBoard
            return ['1', 'mcb']

        mwf_regex = re.search(r'Powered by(.*?)mwForum(.*?)Markus Wichitill', hstring)
        if mwf_regex != None:
            # mwForum
            return ['1', 'mvnf']

        mvn_regex = re.search(r'Powered by(.*?)mvnForum(.*?)</a>', hstring)
        if mvn_regex != None:
            # mvnForum
            return ['1', 'mvnf']

        mupb_regex = re.search(r'Powered by myUPB(.*?)</a>', hstring)
        if mupb_regex != None:
            # myUPB
            return ['1', 'myupb']

        ubbt_regex = re.search(r'>Powered by UBB.threads(.*?)</a>', hstring)
        if ubbt_regex != None:
            # UBB.threads
            return ['1', 'ubbt']

        nnf_regex = re.search(r'Powered by(.*?)NoNonsense Forum</a>', hstring)
        if nnf_regex != None:
            # NoNonsense Forum
            return ['1', 'nnf']

        yaf_regex = re.search(r'>Powered by YAF.NET(.*?)</a>', hstring)
        if yaf_regex != None:
            # Yet Another Forum
            return ['1', 'yaf']

        aef_regex = re.search(r'aefonload(.*?)</script>', hstring, re.DOTALL)
        if aef_regex != None:
            # AEF
            return ['1', 'aef']

        van_regex = re.search(r'applications/vanilla/(.*?).js', hstring)
        if van_regex != None:
            # Vanilla
            return ['1', 'vanilla']

        smf_regex = re.search(r'var smf_(theme_url|images_url|scripturl) =(.*?)</script>', hstring, re.DOTALL)
        if smf_regex != None:
            # SMF
            return ['1', 'smf']

        pun_regex = re.search(r'Powered by(.*?)PunBB</a>', hstring)
        if pun_regex != None:
            # PunBB
            return['1', 'punbb']

        nb_regex = re.search(r'Powered by(.*?)NodeBB</a>', hstring)
        if nb_regex != None:
            # NodeBB
            return['1', 'nodebb']

        myb_regex = re.search(r'(Powered By|href="https://www.mybb.com")(.*?)(MyBB|MyBB Group)</a>', hstring)
        if myb_regex != None:
            # MyBB
            return ['1', 'mybb']

        mb_regex = re.search(r'(powered by|http://www.miniBB.net)(.*?)(miniBB|miniBB forum software)', hstring)
        if mb_regex != None:
            # miniBB
            return ['1', 'minibb']

        fbb_regex = re.search(r'Powered by(.*?)FluxBB', hstring)
        if fbb_regex != None:
            # FluxBB
            return ['1', 'fluxbb']

        ipb_regex = re.search(r'invisioncommunity.com(.*?)Powered by Invision Community', hstring)
        if ipb_regex != None:
            # IP Board
            return['1', 'ipb']

        ipb2_regex = re.search(r'ipb\.(vars|templates|lang)\[(.*?)=(.*?)</script>', hstring, re.DOTALL)
        if ipb2_regex != None:
            # IP Board
            return['1', 'ipb']

        bb_regex = re.search(r'(a href="http://www.woltlab.com"|Forum Software|Forensoftware)(.*?)Burning Board(.*?)</strong>', hstring, re.DOTALL)
        if bb_regex != None:
            # Burning Board
            return['1', 'bboard']

        dsc_regex = re.search(r'Discourse\.(.*?)=(.*?)</script>', hstring, re.DOTALL)
        if dsc_regex != None:
            # Discourse
            return ['1', 'dscrs']

        arc_regex = re.search(r'ping.src = node\.href(.*?)</script>', hstring, re.DOTALL)
        if arc_regex != None:
            # Arc Forum
            return ['1', 'arc']

        hippo_regex = re.search(r'binaries/(.*?)/content/gallery/', hstring)
        if hippo_regex != None:
            # Hippo CMS
            return ['1', 'hippo']

        phpc_regex = re.search(r'.php\?m=(.*?)&c=(.*?)&a=(.*?)&catid=', hstring)
        if phpc_regex != None:
            # phpCMS
            return ['1', 'phpc']

        pb_regex = re.search(r'Powered by (.*?)phpBB', hstring)
        if pb_regex != None:
            # phpBB
            return ['1', 'phpbb']

        pb_regex = re.search(r'copyright(.*?)phpBB Group', hstring)
        if pb_regex != None:
            # phpBB
            return ['1', 'phpbb']

        coton_regex = re.search(r'Powered by(.*?)Cotonti', hstring)
        if coton_regex != None:
            # Cotonti
            return ['1', 'coton']

        con_regex = re.search(r'CCM_(.*?)(_|)(MODE|URL|PATH|FILENAME|REL|CID)', hstring)
        if con_regex != None:
            # Concrete5 CMS
            return ['1', 'con5']

        else:
            # Failure
            return ['0', 'na']
