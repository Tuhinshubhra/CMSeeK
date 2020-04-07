#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

# Precise and Hawt

from html.parser import HTMLParser
import cmseekdb.basic as cmseek

ga = '0'
ga_content = ''

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if 'meta' in tag.lower():
            for nm,vl in attrs:
                if nm == "name" and vl.lower() == 'generator':
                    for a,b in attrs:
                        if a == 'content':
                            global ga, ga_content
                            ga = '1'
                            ga_content += ' ' + b

def parse(source):
    # clean up ga, ga_content (fix some weird multiple sites scan issue)
    global ga, ga_content
    ga = '0'
    ga_content = ''
    parser = MyHTMLParser()
    parser.feed(source)
    return [ga, ga_content]

def scan(content):
    hstring = content.lower()
    if content == '':
        return ['0', '']

    generator_tag_detection_keys = ['wordpress:-wp',
                'blogger:-blg',
                'ghost:-ghost',
                'asciidoc:-asciid',
                'drupal:-dru',
                'bolt:-bolt',
                'browsercms:-brcms',
                'ckan:-ckan',
                'cms made simple:-cmds',
                'cmsimple:-csim',
                'xpressengine:-xe',
                'typo3 cms:-tp3',
                'textpattern cms:-tpc',
                'ametys cms open source (http://www.ametys.org:-amcms',
                'joomla! - open source content management||Joomla! - the dynamic portal engine and content management system||joomla:-joom',
                'xoops:-xoops',
                'wix.com:-wix',
                'cms: website baker||www.websitebaker.org:-wb',
                'webgui:-wgui',
                'subrion cms:-subcms',
                'tiki wiki cms groupware||http://tiki.org:-tiki',
                'snews:-snews',
                'silverstripe:-sst',
                'silva:-silva',
                'serendipity:-spity',
                'seamless.cms.webgui:-slcms',
                'rock:-rock',
                'roadiz:-roadz',
                'ritecms:-rite',
                'rcms:-rcms',
                'quick.cms:-quick',
                'phpwind:-pwind',
                'percussion:-percms',
                'ophal||ophal.org:-ophal',
                'odoo:-odoo',
                'sitefinity:-sfy',
                'microsoft sharePoint:-share',
                'mura cms:-mura',
                'mambo:-mambo',
                'koken:-koken',
                'indexhibit:-ibit',
                'webflow:-wflow',
                'jalios jcms:-jcms',
                'impresspages cms:-impage',
                'hotaru cms:-hotaru',
                'gravcms:-grav',
                'getsimple:-gsimp',
                'fork cms:-fork',
                'php-nuke:-phpn',
                'flexcmp:-flex',
                'ez publish:-ezpu',
                'episerver:-epis',
                'dotnetnuke:-dnn',
                'seomatic:-craft',
                'cpg dragonfly cms:-dragon',
                'cotonti:-coton',
                'orchard:-orchd',
                'contentbox:-cbox',
                'contensis cms:-cntsis',
                'contenido:-cnido',
                'contao:-contao',
                'concrete5:-con5',
                'discourse:-dscrs',
                'discuz!:-discuz',
                'uknowva:-uknva',
                'beehive forum:-bhf',
                'ubb.threads:-ubbt',
                'cubecart:-cubec',
                'dynamicweb:-dweb',
                'ez publish:-ezpub',
                'prestashop:-presta',
                'proximis omnichannel:-pmoc',
                'quick.cart:-qcart',
                'rbs change:-rbsc',
                'sazito:-sazito',
                'shopfa:-shopfa',
                'solusquare:-solusquare',
                'amiro.cms||www.amiro.ru:-amiro',
                'starfield technologies; go daddy website builder:-godaddywb',
                'opennemas:-opennemas',
                'zen-cart.com||zen cart:-zencart'
    ]

    for detection_key in generator_tag_detection_keys:
        if ':-' in detection_key:
            detection_array = detection_key.split(':-')
            if '||' in detection_array[0]:
                detection_strings = detection_array[0].split('||')
                for detection_string in detection_strings:
                    if detection_string in hstring and detection_array[1] not in cmseek.ignore_cms:
                        if cmseek.strict_cms == [] or detection_array[1] in cmseek.strict_cms:
                            return ['1', detection_array[1]]
            else:
                if detection_array[0] in hstring and detection_array[1] not in cmseek.ignore_cms:
                    if cmseek.strict_cms == [] or detection_array[1] in cmseek.strict_cms:
                        return ['1', detection_array[1]]

    return ['0', '']
