#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

### All WordPress DeepScan stuffs goes here

import cmseekdb.basic as cmseek ## Good old module
import VersionDetect.wp as wordpress_version_detect
import deepscans.wp.userenum as wp_user_enum
import deepscans.wp.vuln as wp_vuln_scan
import deepscans.wp.pluginsdetect as wp_plugins_enum
import deepscans.wp.themedetect as wp_theme_enum
import deepscans.wp.pathdisc as path_disclosure
import deepscans.wp.check_reg as check_reg
import cmseekdb.result as sresult
import time
import re
import os

def start(id, url, ua, ga, source, detection_method):
    '''
    id = ID of the cms
    url = URL of target
    ua = User Agent
    ga = [0/1] is GENERATOR meta tag available
    source = source code
    '''

    ## Do shits later [update from later: i forgot what shit i had to do ;___;]
    if id == "wp":
        # referenced before assignment fix
        vulnss = version = wpvdbres = result = plugins_found = usernames = usernamesgen = '0'

        cmseek.statement('Starting WordPress DeepScan')


        # Check if site really is WordPress
        if detection_method == 'source':
            # well most of the wordpress false positives are from source detections.
            cmseek.statement('Checking if the detection is false positive')
            temp_domain = re.findall('^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n\?\=]+)', url)[0]
            wp_match_pattern = temp_domain + '\/wp-(content|include|admin)\/'
            if not re.search(wp_match_pattern, source):
                cmseek.error('Detection was false positive! CMSeeK is quitting!')
                cmseek.success('Run CMSeeK with {0}{1}{2} argument next time'.format(cmseek.fgreen, '--ignore-cms wp', cmseek.cln))
                #cmseek.handle_quit()
                return

        # Version detection
        version = wordpress_version_detect.start(id, url, ua, ga, source)

        ## Check for minor stuffs like licesnse readme and some open directory checks
        cmseek.statement("Initiating open directory and files check")

        ## Readme.html
        readmesrc = cmseek.getsource(url + '/readme.html', ua)
        if readmesrc[0] != '1': ## something went wrong while getting the source codes
            cmseek.statement("Couldn't get readme file's source code most likely it's not present")
            readmefile = '0' # Error Getting Readme file
        elif 'Welcome. WordPress is a very special project to me.' in readmesrc[1]:
            readmefile = '1' # Readme file present
        else:
            readmefile = '2' # Readme file found but most likely it's not of wordpress

        ## license.txt
        licsrc = cmseek.getsource(url + '/license.txt', ua)
        if licsrc[0] != '1':
            cmseek.statement('license file not found')
            licfile = '0'
        elif 'WordPress - Web publishing software' in licsrc[1]:
            licfile = '1'
        else:
            licfile = '2'

        ## wp-content/uploads/ folder
        wpupsrc = cmseek.getsource(url + '/wp-content/uploads/', ua)
        if wpupsrc[0] != '1':
            wpupdir = '0'
        elif 'Index of /wp-content/uploads' in wpupsrc[1]:
            wpupdir = '1'
        else:
            wpupdir = '2'

        ## xmlrpc
        xmlrpcsrc = cmseek.getsource(url + '/xmlrpc.php', ua)
        if xmlrpcsrc[0] != '1':
            cmseek.statement('XML-RPC interface not available')
            xmlrpc = '0'
        elif 'XML-RPC server accepts POST requests only.' in xmlrpcsrc[1]:
            xmlrpc = '1'
        else:
            xmlrpc = '2'

        ## Path disclosure
        cmseek.statement('Looking for potential path disclosure')
        path = path_disclosure.start(url, ua)
        if path != "":
            cmseek.success('Path disclosure detected, path: ' + cmseek.bold + path + cmseek.cln)

        ## Check for user registration
        usereg = check_reg.start(url,ua)
        reg_found = usereg[0]
        reg_url = usereg[1]

        ## Plugins Enumeration
        plug_enum = wp_plugins_enum.start(source)
        plugins_found = plug_enum[0]
        plugins = plug_enum[1]

        ## Themes Enumeration
        theme_enum = wp_theme_enum.start(source,url,ua)
        themes_found = theme_enum[0]
        themes = theme_enum[1]

        ## User enumeration
        uenum = wp_user_enum.start(id, url, ua, ga, source)
        usernamesgen = uenum[0]
        usernames = uenum[1]

        ## Version Vulnerability Detection
        if version != '0':
            version_vuln = wp_vuln_scan.start(version, ua)
            wpvdbres = version_vuln[0]
            result = version_vuln[1]
            if wpvdbres != '0' and version != '0':
                vulnss = len(result['vulnerabilities'])
            vfc = version_vuln[2]

        ### Deep Scan Results comes here
        comptime = round(time.time() - cmseek.cstart, 2)
        log_file = os.path.join(cmseek.log_dir, 'cms.json')
        cmseek.clearscreen()
        cmseek.banner("Deep Scan Results")
        sresult.target(url)
        sresult.cms('WordPress', version, 'https://wordpress.org')
        #cmseek.result("Detected CMS: ", 'WordPress')
        cmseek.update_log('cms_name','WordPress') # update log
        #cmseek.result("CMS URL: ", "https://wordpress.org")
        cmseek.update_log('cms_url', "https://wordpress.org") # update log

        sresult.menu('[WordPress Deepscan]')
        item_initiated = False
        item_ended = False


        if readmefile == '1':
            sresult.init_item("Readme file found: " + cmseek.fgreen + url + '/readme.html' + cmseek.cln)
            cmseek.update_log('wp_readme_file',url + '/readme.html')
            item_initiated = True


        if licfile == '1':
            cmseek.update_log('wp_license', url + '/license.txt')
            if item_initiated == False:
                sresult.init_item("License file: " + cmseek.fgreen + url + '/license.txt' + cmseek.cln)
            else:
                sresult.item("License file: " + cmseek.fgreen + url + '/license.txt' + cmseek.cln)

        if wpvdbres == '1':
            if item_initiated == False:
                sresult.init_item('Changelog: ' + cmseek.fgreen + str(result['changelog_url']) + cmseek.cln)
            else:
                sresult.item('Changelog: ' + cmseek.fgreen + str(result['changelog_url']) + cmseek.cln)
            cmseek.update_log('wp_changelog_file',str(result['changelog_url']))

        if wpupdir == '1':
            cmseek.update_log('wp_uploads_directory',url + '/wp-content/uploads')
            if item_initiated == False:
                sresult.init_item("Uploads directory has listing enabled: " + cmseek.fgreen + url + '/wp-content/uploads' + cmseek.cln)
            else:
                sresult.item("Uploads directory has listing enabled: " + cmseek.fgreen + url + '/wp-content/uploads' + cmseek.cln)


        if xmlrpc == '1':
            cmseek.update_log('xmlrpc', url + '/xmlrpc.php')
            if item_initiated == False:
                sresult.init_item("XML-RPC interface: "+ cmseek.fgreen + url + '/xmlrpc.php' + cmseek.cln)
            else:
                sresult.item("XML-RPC interface: " + cmseek.fgreen + url + '/xmlrpc.php' + cmseek.cln)


        if reg_found == '1':
            sresult.item('User registration enabled: ' + cmseek.bold + cmseek.fgreen + reg_url + cmseek.cln)
            cmseek.update_log('user_registration', reg_url)


        if path != "":
            sresult.item('Path disclosure: ' + cmseek.bold + cmseek.orange + path + cmseek.cln)
            cmseek.update_log('path', path)


        if plugins_found != 0:
            plugs_count = len(plugins)
            sresult.init_item("Plugins Enumerated: " + cmseek.bold + cmseek.fgreen + str(plugs_count) + cmseek.cln)
            wpplugs = ""
            for i, plugin in enumerate(plugins):
                plug = plugin.split(':')
                wpplugs = wpplugs + plug[0] + ' Version ' + plug[1] + ','
                if i == 0 and i != plugs_count - 1:
                    sresult.init_sub('Plugin: ' + cmseek.bold + cmseek.fgreen + plug[0] + cmseek.cln)
                    sresult.init_subsub('Version: ' + cmseek.bold + cmseek.fgreen + plug[1] + cmseek.cln)
                    sresult.end_subsub('URL: ' + cmseek.fgreen + url + '/wp-content/plugins/' + plug[0] + cmseek.cln)
                elif i == plugs_count - 1:
                    sresult.empty_sub()
                    sresult.end_sub('Plugin: ' + cmseek.bold + cmseek.fgreen + plug[0] + cmseek.cln)
                    sresult.init_subsub('Version: ' + cmseek.bold + cmseek.fgreen + plug[1] + cmseek.cln, True, False)
                    sresult.end_subsub('URL: ' + cmseek.fgreen + url + '/wp-content/plugins/' + plug[0] + cmseek.cln, True, False)
                else:
                    sresult.empty_sub()
                    sresult.sub_item('Plugin: ' + cmseek.bold + cmseek.fgreen + plug[0] + cmseek.cln)
                    sresult.init_subsub('Version: ' + cmseek.bold + cmseek.fgreen + plug[1] + cmseek.cln)
                    sresult.end_subsub('URL: ' + cmseek.fgreen + url + '/wp-content/plugins/' + plug[0] + cmseek.cln)
            cmseek.update_log('wp_plugins', wpplugs)
            sresult.empty_item()

        if themes_found != 0:
            thms_count = len(themes)
            sresult.init_item("Themes Enumerated: " + cmseek.bold + cmseek.fgreen + str(thms_count) + cmseek.cln)
            wpthms = ""
            for i,theme in enumerate(themes):
                thm = theme.split(':')
                thmz = thm[1].split('|')
                wpthms = wpthms + thm[0] + ' Version ' + thmz[0] + ','
                if i == 0 and i != thms_count - 1:
                    sresult.init_sub('Theme: ' + cmseek.bold + cmseek.fgreen + thm[0] + cmseek.cln)
                    sresult.init_subsub('Version: ' + cmseek.bold + cmseek.fgreen + thmz[0] + cmseek.cln)
                    if thmz[1] != '':
                        sresult.subsub('Theme Zip: ' + cmseek.bold + cmseek.fgreen + url + thmz[1] + cmseek.cln)
                    sresult.end_subsub('URL: ' + cmseek.fgreen + url + '/wp-content/themes/' + thm[0] + cmseek.cln)
                elif i == thms_count - 1:
                    sresult.empty_sub(True)
                    sresult.end_sub('Theme: ' + cmseek.bold + cmseek.fgreen + thm[0] + cmseek.cln)
                    sresult.init_subsub('Version: ' + cmseek.bold + cmseek.fgreen + thmz[0] + cmseek.cln, True, False)
                    if thmz[1] != '':
                        sresult.subsub('Theme Zip: ' + cmseek.bold + cmseek.fgreen + url + thmz[1] + cmseek.cln, True, False)
                    sresult.end_subsub('URL: ' + cmseek.fgreen + url + '/wp-content/themes/' + thm[0] + cmseek.cln, True, False)
                else:
                    sresult.sub_item('Theme: ' + cmseek.bold + cmseek.fgreen + thm[0] + cmseek.cln)
                    sresult.init_subsub('Version: ' + cmseek.bold + cmseek.fgreen + thmz[0] + cmseek.cln)
                    if thmz[1] != '':
                        sresult.subsub('Theme Zip: ' + cmseek.bold + cmseek.fgreen + url + thmz[1] + cmseek.cln)
                    sresult.end_subsub('URL: ' + cmseek.fgreen + url + '/wp-content/themes/' + thm[0] + cmseek.cln)
            cmseek.update_log('wp_themes', wpthms)
            sresult.empty_item()


        if usernamesgen == '1':
            user_count = len(usernames)
            sresult.init_item("Usernames harvested: " + cmseek.bold + cmseek.fgreen + str(user_count) + cmseek.cln)
            wpunames = ""
            for i,u in enumerate(usernames):
                wpunames = wpunames + u + ","
                if i == 0 and i != user_count - 1:
                    sresult.init_sub(cmseek.bold + cmseek.fgreen + u + cmseek.cln)
                elif i == user_count - 1:
                    sresult.end_sub(cmseek.bold + cmseek.fgreen + u + cmseek.cln)
                else:
                    sresult.sub_item(cmseek.bold + cmseek.fgreen + u + cmseek.cln)
            cmseek.update_log('wp_users', wpunames)
            sresult.empty_item()

        if version != '0':
            # cmseek.result("Version: ", version)
            cmseek.update_log('wp_version', version)
            if wpvdbres == '1':
                sresult.end_item('Version vulnerabilities: ' + cmseek.bold + cmseek.fgreen + str(vulnss) + cmseek.cln)
                cmseek.update_log('wp_vuln_count', str(vulnss))
                cmseek.update_log("wp_vulns", result, False)
                if vulnss > 0:
                    for i,vuln in enumerate(result['vulnerabilities']):
                        if i == 0 and i != vulnss - 1:
                            sresult.empty_sub(False)
                            sresult.init_sub(cmseek.bold + cmseek.fgreen + str(vuln['name']) + cmseek.cln, False)
                            # sresult.init_subsub("Type: " + cmseek.bold + cmseek.fgreen + str(vuln['vuln_type']) + cmseek.cln, False, True)
                            # sresult.subsub("Link: " + cmseek.bold + cmseek.fgreen + "http://wpvulndb.com/vulnerabilities/" + str(vuln['id']) + cmseek.cln, False, True)
                            strvuln = str(vuln)
                            if vuln['cve'] != "":
                                sresult.subsub("CVE: " + cmseek.fgreen + "http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-" + vuln["cve"] + cmseek.cln, False, True)

                            '''
                            if 'exploitdb' in strvuln:
                                for ref in vuln['references']['exploitdb']:
                                    sresult.subsub("ExploitDB Link: " + cmseek.fgreen + "http://www.exploit-db.com/exploits/" + str(ref) + cmseek.cln, False, True)

                            if 'metasploit' in strvuln:
                                for ref in vuln['references']['metasploit']:
                                    sresult.subsub("Metasploit Module: " + cmseek.fgreen + "http://www.metasploit.com/modules/" + str(ref) + cmseek.cln, False, True)

                            if 'osvdb' in strvuln:
                                for ref in vuln['references']['osvdb']:
                                    sresult.subsub("OSVDB Link: " + cmseek.fgreen + "http://osvdb.org/" + str(ref) + cmseek.cln, False, True)

                            if 'secunia' in strvuln:
                                for ref in vuln['references']['secunia']:
                                    sresult.subsub("Secunia Advisory: " + cmseek.fgreen + "http://secunia.com/advisories/" + str(ref) + cmseek.cln, False, True)
                            
                            if 'url' in strvuln:
                                for ref in vuln['references']['url']:
                                    sresult.subsub("Reference: " + cmseek.fgreen + str(ref) + cmseek.cln, False, True)
                            '''
                            if vuln["references"] != []:
                                for ref in vuln["references"]:
                                    sresult.subsub("Reference: " + cmseek.fgreen + str(ref) + cmseek.cln, False, True)
                            sresult.end_subsub("Fixed In Version: " + cmseek.bold + cmseek.fgreen + str(vuln['fixed_in']) + cmseek.cln, False, True)

                        elif i == vulnss - 1:
                            sresult.empty_sub(False)
                            sresult.end_sub(cmseek.bold + cmseek.fgreen + str(vuln['name']) + cmseek.cln, False)
                            # sresult.init_subsub("Type: " + cmseek.bold + cmseek.fgreen + str(vuln['vuln_type']) + cmseek.cln, False, False)
                            # sresult.subsub("Link: " + cmseek.bold + cmseek.fgreen + "http://wpvulndb.com/vulnerabilities/" + str(vuln['id']) + cmseek.cln, False, False)
                            strvuln = str(vuln)
                            if vuln['cve'] != "":
                                sresult.subsub("CVE: " + cmseek.fgreen + "http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-" + vuln["cve"] + cmseek.cln, False, False)

                            if vuln["references"] != []:
                                for ref in vuln["references"]:
                                    sresult.subsub("Reference: " + cmseek.fgreen + str(ref) + cmseek.cln, False, False)

                            sresult.end_subsub("Fixed In Version: " + cmseek.bold + cmseek.fgreen + str(vuln['fixed_in']) + cmseek.cln, False, False)
                        else:
                            sresult.empty_sub(False)
                            sresult.sub_item(cmseek.bold + cmseek.fgreen + str(vuln['name']) + cmseek.cln, False)
                            #sresult.init_subsub("Type: " + cmseek.bold + cmseek.fgreen + str(vuln['vuln_type']) + cmseek.cln, False, True)
                            #sresult.subsub("Link: " + cmseek.bold + cmseek.fgreen + "http://wpvulndb.com/vulnerabilities/" + str(vuln['id']) + cmseek.cln, False, True)
                            strvuln = str(vuln)
                            if vuln['cve'] != "":
                                sresult.subsub("CVE: " + cmseek.fgreen + "http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-" + str(ref) + cmseek.cln, False, True)
                                    

                            if vuln["references"] != []:
                                for ref in vuln["references"]:
                                    sresult.subsub("Reference: " + cmseek.fgreen + str(ref) + cmseek.cln, False, True)

                            sresult.end_subsub("Fixed In Version: " + cmseek.bold + cmseek.fgreen + str(vuln['fixed_in']) + cmseek.cln, False, True)
        sresult.end(str(cmseek.total_requests), str(comptime), log_file)
        return


    return
