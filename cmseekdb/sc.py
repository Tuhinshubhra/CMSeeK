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

        elif 'WebFontConfig = ' in hstring:
            # Bubble CMS
            return ['1','bubble']

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

        elif '"beacon":"bam.nr-data.net"' in hstring or 'simplebo.net/' in hstring  or '"pswp__' in hstring:
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

        phpc_regex = re.search(r'.php\?m=(.*?)&c=(.*?)&a=(.*?)&catid=', hstring)
        if phpc_regex != None:
            # phpCMS
            return ['1', 'phpc']

        else:
            # Failure
            return ['0', 'na']
