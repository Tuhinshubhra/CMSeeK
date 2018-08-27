#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 Tuhinshubhra

# Precise and Hawt

from html.parser import HTMLParser

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
    content = content.lower()
    if content == '':
        return ['0', '']

    if 'wordpress' in content:
        # WordPress
        r = ['1','wp']
        return r

    if 'blogger' in content:
        # Blogger by google
        r = ['1','blg']
        return r

    if 'ghost' in content:
        # Ghost CMS
        r = ['1','ghost']
        return r

    if 'asciidoc' in content:
        # ASCiiDOC
        r = ['1','asciid']
        return r

    if 'drupal' in content:
        # Drupal
        r = ['1','dru']
        return r

    if 'bolt' in content:
        # Bolt CMS
        r = ['1','bolt']
        return r

    if 'browsercms' in content:
        # Browser CMS
        r = ['1','brcms']
        return r

    if 'ckan' in content:
        # CKAN
        r = ['1','ckan']
        return r

    if 'cms made simple' in content:
        # CMS Made Simple
        r = ['1','cmds']
        return r

    if 'cmsimple' in content:
        # CMSimple
        r = ['1','csim']
        return r

    if 'xpressengine' in content:
        # XpressEngine
        r = ['1','xe']
        return r

    if 'typo3 cms' in content:
        # TYPO3 CMS
        r = ['1','tp3']
        return r

    if 'textpattern cms' in content:
        # Textpattern CMS
        r = ['1','tpc']
        return r

    if 'ametys cms open source (http://www.ametys.org' in content:
        # Ametys CMS
        r = ['1','amcms']
        return r

    if 'joomla! - open source content management' in content or 'Joomla! - the dynamic portal engine and content management system' in content or 'joomla' in content:
        # Joomla
        r = ['1', 'joom']
        return r

    if 'xoops' in content:
        # XOOPS
        r = ['1', 'xoops']
        return r

    if 'wix.com' in content:
        # Wix Website Builder
        return ['1', 'wix']

    if 'cms: website baker' in content or 'www.websitebaker.org' in content:
        # Website Baker
        return ['1', 'wb']

    if 'webgui' in content:
        # WebGUI
        return ['1', 'wgui']

    if 'subrion cms' in content:
        # Subrion CMS
        return ['1', 'subcms']

    if 'tiki wiki cms groupware' in content or 'http://tiki.org' in content:
        # Tiki Wiki CMS Groupware
        return ['1', 'tiki']

    if 'snews' in content:
        # sNews
        return ['1', 'snews']

    if 'silverstripe' in content:
        # SilverStripe
        return ['1', 'sst']

    if 'silva' in content:
        # Silva CMS
        return ['1', 'silva']

    if 'serendipity' in content:
        # Serendipity
        return ['1', 'spity']

    if 'seamless.cms.webgui' in content:
        # SeamlessCMS
        return ['1', 'slcms']

    if 'rock' in content:
        # RockRMS
        return ['1', 'rock']

    if 'roadiz' in content:
        # Roadiz CMS
        return ['1', 'roadz']

    if 'ritecms' in content:
        # RiteCMS
        return ['1', 'rite']

    if content == 'rcms':
        # RCMS
        return ['1', 'rcms']

    if 'quick.cms' in content:
        # Quick.Cms
        return ['1', 'quick']

    if 'phpwind' in content:
        # phpWind
        return ['1', 'pwind']

    if 'percussion' in content:
        # Percussion CMS
        return ['1', 'percms']

    if 'ophal' in content or 'ophal.org' in content:
        # Ophal
        return ['1', 'ophal']

    if content == 'odoo':
        # Odoo
        return ['1', 'odoo']

    if 'sitefinity' in content:
        # Sitefinity
        return ['1', 'sfy']

    if 'microsoft sharePoint' in content:
        # Microsoft SharePoint
        return ['1', 'share']

    if 'mura cms' in content:
        # Mura CMS
        return ['1', 'mura']

    if 'mambo' in content:
        # Mambo
        return ['1', 'mambo']

    if 'koken' in content:
        # Koken
        return ['1', 'koken']

    if 'indexhibit' in content:
        # Indexhibit
        return ['1', 'ibit']

    if 'webflow' in content:
        # Webflow CMS
        return ['1', 'wflow']

    if 'jalios jcms' in content:
        # Jalios JCMS
        return ['1', 'jcms']

    if 'impresspages cms' in content:
        # ImpressPages CMS
        return ['1', 'impage']

    if 'hotaru cms' in content:
        # Hotaru CMS
        return ['1', 'hotaru']

    if 'gravcms' in content:
        # GravCMS
        return ['1', 'grav']

    if 'getsimple' in content:
        # GetSimple CMS
        return ['1', 'gsimp']

    if 'fork cms' in content:
        # Fork CMS
        return ['1', 'fork']

    if 'php-nuke' in content:
        # PHP Nuke
        return ['1', 'phpn']

    if 'flexcmp' in content:
        # FlexCMP
        return ['1', 'flex']

    if 'ez publish' in content:
        # eZ Publish
        return ['1', 'ezpu']

    if 'episerver' in content:
        # EPiServer
        return ['1', 'epis']

    if 'dotnetnuke' in content:
        # DNN Platform
        return ['1', 'dnn']

    if 'seomatic' in content:
        # SEOmatic is a Craft CMS plugin so..
        return ['1', 'craft']

    if 'cpg dragonfly cms' in content:
        # CPG Dragonfly
        return['1', 'dragon']

    if 'cotonti' in content:
        # Cotonti
        return ['1', 'coton']

    if 'orchard' in content:
        # Orchard CMS
        return ['1', 'orchd']

    if 'contentbox' in content:
        # ContentBox
        return ['1', 'cbox']

    if 'contensis cms' in content:
        # Contensis CMS
        return ['1', 'cntsis']

    if 'contenido' in content:
        # CMS Contenido 
        return ['1', 'cnido']

    if 'contao' in content:
        # Contao CMS
        return ['1', 'contao']

    if 'concrete5' in content:
        # concrete5 CMS
        return ['1', 'con5']

    if 'discourse' in content:
        # Discourse
        return ['1', 'dscrs']

    if 'discuz!' in content:
        # Discuz
        return ['1', 'discuz']

    if 'uknowva' in content:
        # uKnowva
        return ['1', 'uknva']

    if 'beehive forum' in content:
        # Beehive Forum
        return ['1', 'bhf']

    if 'ubb.threads' in content:
        # UBB.threads
        return ['1', 'ubbt']

    return ['0', '']
