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

        detkeys = [
        "/wp-content/:-wp",
        "/skin/frontend/||x-magento-init:-mg",
        "https://www.blogger.com/static/:-blg",
        "ic.pics.livejournal.com:-lj",
        "END: 3dcart stats:-tdc",
        "href=\"/apos-minified/:-apos",
        "href=\"/CatalystStyles/:-abc",
        "src=\"/misc/drupal.js\":-dru",
        "css/joomla.css:-joom",
        "Powered By <a href=\"http://www.opencart.com\">OpenCart||\"catalog/view/javascript/jquery/swiper/css/opencart.css\"||index.php?route=:-oc",
        "/xoops.js||xoops_redirect:-xoops",
        "Wolf Default RSS Feed:-wolf",
        "/ushahidi.js||alt=\"Ushahidi\":-ushahidi",
        "getWebguiProperty:-wgui",
        "title: \"TiddlyWiki\"||TiddlyWiki created by Jeremy Ruston,:-tidw",
        "Running Squiz Matrix:-sqm",
        "assets.spin-cdn.com:-spin",
        "content=\"Solodev\" name=\"author\":-sdev",
        "content=\"sNews:-snews",
        "/api/sitecore/:-score",
        "simsite/:-sim",
        "simplebo.net/ ||\"pswp__:-spb",
        "/silvatheme:-silva",
        "serendipityQuickSearchTermField ||\"serendipity_||serendipity[:-spity",
        "Published by Seamless.CMS.WebUI:-slcms",
        "rock-config-trigger||rock-config-cancel-trigger:-rock",
        "/rcms-f-production.:-rcms",
        "CMS by Quick.Cms||read license: www.opensolution.org/license.html:-quick",
        "\"pimcore_:-pcore",
        "xmlns:perc||cm/css/perc_decoration.css:-percms",
        "PencilBlueController||\"pencilblueApp\":-pblue",
        "/libraries/ophal.js:-ophal",
        "Sitefinity/WebsiteTemplates:-sfy",
        "published by Open Text Web Solutions:-otwsm",
        "/opencms/export/:-ocms",
        "odoo.session_info||var odoo =:-odoo",
        "_spBodyOnLoadWrapper||_spPageContextInfo||_spFormOnSubmitWrapper:-share",
        "/storage/app/media/:-octcms",
        "mura.min.css||/plugins/Mura:-mura",
        "mt-content/||moto-website-style:-moto",
        "mono_donottrack||monotracker.js ||_monoTracker:-mnet",
        "Powered by MODX</a>:-modx",
        "siteCMS:methode\"||\"contentOriginatingCMS=Methode\"||Methode tags version||/r/PortalConfig/common/assets/:-methd",
        "var LIVESTREET_SECURITY_KEY:-lscms",
        "/koken.js||data-koken-internal:-koken",
        "jimdo_layout_css||var jimdoData||isJimdoMobileApp:-jimdo",
        "<!-- you must provide a link to Indexhibit||\"Built with <a href=http://www.indexhibit.org/>Indexhibit\"||ndxz-studio/site||ndxzsite/:-ibit",
        "<!-- webflow css -->||css/webflow.css||js/webflow.js:-wflow",
        "css/jalios/core/||js/jalios/core/||jalios:ready:-jcms",
        "ip_themes/||ip_libs/||ip_cms/:-impage",
        "/css_js_cache/hotaru_css||hotaruFooterImg||/css_js_cache/hotaru_js:-hotaru",
        "binaries/content/gallery/:-hippo",
        "PHP-Nuke Copyright ©||PHP-Nuke theme by:-phpn",
        "FlexCMP - CMS per Siti Accessibili||/flex/TemplatesUSR/||FlexCMP - Digital Experience Platform (DXP):-flex",
        "copyright\" content=\"eZ Systems\"||ezcontentnavigationpart||ezinfo/copyright:-ezpu",
        "e107_files/e107.js||e107_themes/||e107_plugins/:-e107",
        "<!-- DNN Platform|| by DNN Corporation -->||DNNROBOTS||js/dnncore.js?||dnn_ContentPane||js/dnn.js?:-dnn",
        "phpBBstyle||phpBBMobileStyle||style_cookie_settings:-phpbb",
        "dede_fields||dede_fieldshash||DedeAjax||DedeXHTTP||include/dedeajax2.js||css/dedecms.css:-dede",
        "/Orchard.jQuery/||orchard.themes||orchard-layouts-root:-orchd",
        "modules/contentbox/themes/:-cbox",
        "data-contentful||.contentful.com/||.ctfassets.net/:-conful",
        "Contensis.current||ContensisSubmitFromTextbox||ContensisTextOnly:-contensis",
        "system/cron/cron.txt:-contao",
        "/burningBoard.css||wcf/style/:-bboard",
        "/concrete/images||/concrete/css||/concrete/js:-con5",
        "discourse_theme_id||discourse_current_homepage:-discrs",
        "discuz_uid||discuz_tips||content=\"Discuz! Team and Comsenz UI Team\":-discuz",
        "flarum-loading||flarum/app:-flarum",
        "/* IP.Board||js/ipb.js||js/ipb.lang.js:-ipb",
        "ips_usernameand ips_password:-ipb",
        "bb_default_style.css||name=\"URL\" content=\"http://www.minibb.net/\":-minibb",
        "var MyBBEditor:-mybb",
        "/assets/nodebb.min.js||/plugins/nodebb-:-nodebb",
        "PUNBB.env||typeof PUNBB ===:-punbb",
        "Powered by SMF:-smf",
        "vanilla_discussions_index||vanilla_categories_index:-vanilla",
        "Forum software by XenForo&trade;||<html id=\"XenForo\"||css.php?css=xenforo:-xf",
        "<!-- Powered by XMB||<!-- The XMB Group -->||Powered by XMB:-xmb",
        "yabbfiles/:-yabb",
        "Powered By AEF:-aef",
        "Powered by: FUDforum:-fudf",
        "<div id=\"phorum\">:-phorum",
        "\"YafHead:-yaf",
        "<!-- NoNonsense Forum:-nnf",
        "/mvnplugin/mvnforum/:-mvnf",
        "aspnetforum.css\"||_AspNetForumContentPlaceHolder:-aspf",
        "jforum/templates/:-jf",
        "This OnlineStore is brought to you by ViA-Online GmbH Afterbuy.:-abuy",
        '/arastta.js:-arstta',
        '<script src=\'//bizweb.dktcdn.net:-bizw',
        'cloudcart","title:-cloudc',
        'framework/colormekit.css:-cmshop'
        ]

        for keyl in detkeys:
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

        rgxkeys = [
        '(\'|")https\://afosto\-cdn(.*?)\.afosto\.com(.*?)(\'|"):-afsto',
        'Powered by(.*?)JForum(.*?)\</a\>:-jf',
        'Powered by(.*?)AspNetForum(.*?)(\</a\>|\</span\>):-aspf',
        'Powered by(.*?)MercuryBoard(.*?)\</a\>:-mcb',
        'Powered by(.*?)mwForum(.*?)Markus Wichitill:-mvnf',
        'Powered by(.*?)mvnForum(.*?)\</a\>:-mvnf',
        'Powered by myUPB(.*?)\</a\>:-myupb',
        '\>Powered by UBB\.threads(.*?)\</a\>:-ubbt',
        'Powered by(.*?)NoNonsense Forum\</a\>:-nnf',
        '\>Powered by YAF\.NET(.*?)\</a\>:-yaf',
        'aefonload(.*?)\</script\>:-aef',
        'applications/vanilla/(.*?)\.js:-vanilla',
        'var smf_(theme_url|images_url|scripturl) \=(.*?)\</script\>:-smf',
        'Powered by(.*?)PunBB\</a\>:-punbb',
        'Powered by(.*?)NodeBB\</a\>:-nodebb',
        '(Powered By|href\="https\://www\.mybb\.com")(.*?)(MyBB|MyBB Group)\</a\>:-mybb',
        '(powered by|http\://www\.miniBB\.net)(.*?)(miniBB|miniBB forum software):-minibb',
        'Powered by(.*?)FluxBB:-fluxbb',
        'invisioncommunity\.com(.*?)Powered by Invision Community:-ipb',
        'ipb\.(vars|templates|lang)\[(.*?)=(.*?)\</script\>:-ipb',
        '(a href\="http\://www\.woltlab\.com"|Forum Software|Forensoftware)(.*?)Burning Board(.*?)\</strong\>:-bboard',
        'Discourse\.(.*?)\=(.*?)\</script\>:-dscrs',
        'ping\.src \= node\.href(.*?)\</script\>:-arc',
        'binaries/(.*?)/content/gallery/:-hippo',
        '\.php\?m\=(.*?)&c\=(.*?)&a\=(.*?)&catid\=:-phpc',
        'Powered by (.*?)phpBB:-phpbb',
        'copyright(.*?)phpBB Group:-phpbb',
        'Powered by(.*?)Cotonti:-coton',
        'CCM_(.*?)(_|)(MODE|URL|PATH|FILENAME|REL|CID):-con5',
        '\<link href\=(.*?)cdn(\d).bigcommerce\.com\/:-bigc',
        '\<a href\=(.*?)main_bigware_(\d)\.php:-bigw',
        'var Bizweb \=(.*?)\</script\>:-bizw',
        'var clientexec \=(.*?)\</script\>||Powered by(.*?)http\://www\.clientexec\.com\?source\=poweredby(.*?)\</a\>:-cexec',
        '\<meta name\=(.*?)author(.*?)CloudCart LLC(.*?)\>:-cloudc',
        'var Colorme \=(.*?)\</script\>:-cmshop'
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
                        if natero != None:
                            return ['1', hunter[1]]
                else:
                    natero = re.search(hunter[0], hstring, re.DOTALL)
                    if natero != None:
                        return ['1', hunter[1]]

        else:
            # Failure
            return ['0', 'na']
