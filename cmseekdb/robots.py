#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 Tuhinshubhra

# Detect cms using robots.txt
# Rev 1
import re
import cmseekdb.basic as cmseek
def check(url, ua):
    robots = url + '/robots.txt'
    robots_source = cmseek.getsource(robots, ua)
    # print(robots_source[1])
    if robots_source[0] == '1' and robots_source[1] != '':
        # Check begins here
        robotstr = robots_source[1]

        if 'If the Joomla site is installed' in robotstr or 'Disallow: /administrator/' in robotstr:
            return ['1', 'joom']

        if 'Allow: /core/*.css$' in robotstr or 'Disallow: /index.php/user/login/' in robotstr or 'Disallow: /web.config' in robotstr:
            return ['1', 'dru']

        if 'Disallow: /wp-admin/' in robotstr or 'Allow: /wp-admin/admin-ajax.php' in robotstr:
            return ['1', 'wp']

        if 'Disallow: /kernel/' in robotstr and 'Disallow: /language/' in robotstr and 'Disallow: /templates_c/' in robotstr:
            return ['1', 'xoops']

        if 'Disallow: /textpattern' in robotstr:
            return ['1', 'tpc']

        if 'Disallow: /sitecore' in robotstr or 'Disallow: /sitecore_files' in robotstr or 'Disallow: /sitecore modules' in robotstr:
            return ['1', 'score']

        if 'Disallow: /phpcms' in robotstr or 'robots.txt for PHPCMS' in robotstr:
            return ['1', 'phpc']

        if 'Disallow: /*mt-content*' in robotstr or 'Disallow: /mt-includes/' in robotstr:
            return ['1', 'moto']

        if 'Disallow: /jcmsplugin/' in robotstr:
            return ['1', 'jcms']

        if 'Disallow: /ip_cms/' in robotstr or 'ip_backend_frames.php' in robotstr or 'ip_backend_worker.php' in robotstr:
            return ['1', 'impage']

        if 'Disallow: /flex/tmp/' in robotstr or 'flex/Logs/' in robotstr:
            return ['1', 'flex']

        if 'Disallow: /e107_admin/' in robotstr or 'e107_handlers' in robotstr or 'e107_files/cache' in robotstr:
            return ['1', 'e107']

        if 'Disallow: /plus/ad_js.php' in robotstr or 'Disallow: /plus/erraddsave.php' in robotstr or 'Disallow: /plus/posttocar.php' in robotstr or 'Disallow: /plus/disdls.php' in robotstr or 'Disallow: /plus/mytag_js.php' in robotstr or 'Disallow: /plus/stow.php' in robotstr:
            return ['1', 'dede']

        if 'modules/contentbox/themes/' in robotstr:
            return ['1', 'cbox']

        if 'Disallow: /contao/' in robotstr:
            return ['1', 'contao']

        if 'Disallow: /concrete' in robotstr:
            return ['1', 'con5']

        if 'Disallow: /auth/cas' in robotstr and 'Disallow: /auth/cas/callback' in robotstr:
            return ['1', 'dscrs']

        if 'uc_client' in robotstr and 'uc_server' in robotstr and 'forum.php?mod=redirect*' in robotstr:
            return ['1', 'discuz']

        if 'Disallow: /craft/' in robotstr:
            # Chances of it being a falsepositive are higher than the chances of me doing something good with my life ;__;
            return ['1', 'craft']

        t3_regex = re.search(r'Sitemap: http(.*?)\?type=', robotstr)
        if t3_regex != None:
            return ['1', 'tp3']

        return ['0','']
    else:
        cmseek.error('robots.txt not found or empty!')
        return ['0','']
