# This file contains all the methods of detecting cms via Source Code
# This is a part of CMSeeK project
# Version: 1.0.0
# Return a list with ['1'/'0','ID of CMS'/'na'] 1 = detected 0 = not detected 2 = No Sourcecode Provided

def generator(s): ## CMS Check using generator meta tags
    if s == "": ## No source code provided kinda shitty check but oh well
        r = ['2', 'na']
        return r
    else: ## The real shit begins here
        hstring = s
        if 'name="generator" content="WordPress' in hstring:
            # WordPress
            r = ['1','wp']
            return r

        elif "content='blogger' name='generator'/>" in hstring:
            # Blogger by google
            r = ['1','blg']
            return r

        elif '<meta name="generator" content="Ghost' in hstring:
            # Ghost CMS
            r = ['1','ghost']
            return r

        elif '<meta name="generator" content="AsciiDoc' in hstring:
            # ASCiiDOC
            r = ['1','asciid']
            return r

        elif '<meta name="Generator" content="Drupal' in hstring:
            # Drupal
            r = ['1','dru']
            return r

        elif '<meta name="generator" content="Bolt">' in hstring:
            # Bolt CMS
            r = ['1','bolt']
            return r

        elif '<meta name="generator" content="BrowserCMS' in hstring:
            # Browser CMS
            r = ['1','brcms']
            return r

        elif '<meta name="generator" content="ckan' in hstring:
            # CKAN
            r = ['1','ckan']
            return r

        elif '<meta name="generator" content="CMS Made Simple' in hstring:
            # CMS Made Simple
            r = ['1','cmds']
            return r

        elif '<meta name="generator" content="CMSimple' in hstring:
            # CMSimple
            r = ['1','csim']
            return r

        elif '<meta name="Generator" content="XpressEngine' in hstring:
            # XpressEngine
            r = ['1','xe']
            return r

        elif '<meta name="generator" content="TYPO3 CMS"' in hstring:
            # TYPO3 CMS
            r = ['1','tp3']
            return r

        elif '<meta name="generator" content="Textpattern CMS"' in hstring:
            # Textpattern CMS
            r = ['1','tpc']
            return r

        elif 'meta content="Ametys CMS Open source (http://www.ametys.org" name="generator"' in hstring:
            # Ametys CMS
            r = ['1','amcms']
            return r
        elif '<meta name="generator" content="Joomla! - Open Source Content Management' in hstring:
            # Joomla
            r = ['1', 'joom']
            return r

        else:
            # Nothing Found
            r = ['0', 'na']
            return r

def check(s, site): ## Check if no generator meta tag available
    if s == "": ## No source code provided kinda shitty check but oh well
        r = ['2', 'na']
        return r
    else: ## The real shit begins here
        hstring = s
        # harray = s.split("\n") ### Array conversion can use if needed later
        if '/wp-content/' in hstring:
            # WordPress
            r = ['1','wp']
            return r

        elif '/skin/frontend/' or 'x-magento-init' in hstring:
            # Magento
            r = ['1','mg']
            return r

        elif 'https://www.blogger.com/static/' in hstring:
            # Blogger By Google
            r = ['1','blg']
            return r

        elif 'ic.pics.livejournal.com' in hstring:
            # LiveJournal
            r = ['1','lj']
            return r

        elif 'END: 3dcart stats' in hstring:
            # 3D Cart
            r = ['1','tdc']
            return r

        elif 'href="/apos-minified/' in hstring:
            # Apostrophe CMS
            r = ['1','apos']
            return r

        elif 'WebFontConfig = ' in hstring:
            # Bubble CMS
            r = ['1','bubble']
            return r

        elif 'href="/CatalystStyles/' in hstring:
            # Adobe Business Catalyst
            r = ['1','abc']
            return r

        elif 'Joomla' in hstring: # Lamest one possible
            # Obvious Joomla
            r = ['1','joom']
            return r

        elif 'Powered By <a href="http://www.opencart.com">OpenCart' in hstring or "catalog/view/javascript/jquery/swiper/css/opencart.css" in hstring or 'index.php?route=' in hstring:
            # OpenCart
            r = ['1', 'oc']
            return r

        else:
            # Failure
            r = ['0', 'na']
            return r
