#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 Tuhinshubhra

### All WordPress DeepScan stuffs goes here

import cmseekdb.basic as cmseek ## Good old module
import VersionDetect.wp as wordpress_version_detect
import deepscans.wp.userenum as wp_user_enum
import deepscans.wp.vuln as wp_vuln_scan
import deepscans.wp.pluginsdetect as wp_plugins_enum
import deepscans.wp.themedetect as wp_theme_enum
import deepscans.wp.pathdisc as path_disclosure
import deepscans.wp.check_reg as check_reg

def start(id, url, ua, ga, source): ## ({ID of the cms}, {url of target}, {User Agent}, {is Generator Meta tag available [0/1]}, {Source code})
    ## Do shits later [update from later: i forgot what shit i had to do ;___;]
    if id == "wp":
        # referenced before assignment fix
        version = wpvdbres = result = plugins_found = usernames = usernamesgen = '0'

        cmseek.statement('Starting WordPress DeepScan')
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
        version_vuln = wp_vuln_scan.start(version, ua)
        wpvdbres = version_vuln[0]
        result = version_vuln[1]
        vfc = version_vuln[2]

        ### Deep Scan Results comes here
        cmseek.clearscreen()
        cmseek.banner("Deep Scan Results")
        cmseek.result("Detected CMS: ", 'WordPress')
        cmseek.update_log('cms_name','WordPress') # update log
        cmseek.result("CMS URL: ", "https://wordpress.org")
        cmseek.update_log('cms_url', "https://wordpress.org") # update log
        if version != '0':
            cmseek.result("Version: ", version)
            cmseek.update_log('wp_version', version)
        if wpvdbres == '1':
            cmseek.result("Changelog URL: " , str(result['changelog_url']))
            cmseek.update_log('wp_changelog_file',str(result['changelog_url']))
        if reg_found == '1':
            cmseek.result('User registration enabled: ', reg_url)
            cmseek.update_log('user_registration', reg_url)
        if path != "":
            cmseek.result('Path disclosure: ', path)
            cmseek.update_log('path', path)
        if readmefile == '1':
            cmseek.result("Readme file found: ", url + '/readme.html')
            cmseek.update_log('wp_readme_file',url + '/readme.html')
        if licfile == '1':
            cmseek.result("License file found: ", url + '/license.txt')
        if wpupdir == '1':
            cmseek.result("Uploads directory has listing enabled: ", url + '/wp-content/uploads')
            cmseek.update_log('wp_uploads_directory',url + '/wp-content/uploads')
        if xmlrpc == '1':
            cmseek.result("XML-RPC interface available: ", url + '/xmlrpc.php')
            cmseek.update_log('wp_uploads_directory', url + '/xmlrpc.php')
        if plugins_found != 0:
            print('\n')
            cmseek.result("Plugins Enumerated: ", '')
            print(" |")
            wpplugs = ""
            for plugin in plugins:
                plug = plugin.split(':')
                wpplugs = wpplugs + plug[0] + ' Version ' + plug[1] + ','
                cmseek.success(cmseek.bold + plug[0] + ' Version ' + plug[1] + cmseek.cln)
            cmseek.update_log('wp_plugins', wpplugs)
        if themes_found != 0:
            print('\n')
            cmseek.result("themes Enumerated: ", '')
            print(" |")
            wpthms = ""
            for theme in themes:
                thm = theme.split(':')
                thmz = thm[1].split('|')
                wpthms = wpthms + thm[0] + ' Version ' + thmz[0] + ','
                cmseek.success(cmseek.bold + thm[0] + ' Version ' + thmz[0] + cmseek.cln)
                cmseek.result('Theme URL: ', url + '/wp-content/themes/' + thm[0] + '/')
                if thmz[1] != '':
                    cmseek.result('Theme Zip URL: ', url + thmz[1])
            cmseek.update_log('wp_themes', wpthms)
        if usernamesgen == '1':
            print('\n')
            cmseek.result("Usernames Harvested: ",'')
            print(" |")
            wpunames = ""
            for u in usernames:
                wpunames = wpunames + u + ","
                cmseek.success(cmseek.bold + u + cmseek.cln)
            print('\n')
            cmseek.update_log('wp_users', wpunames)
        if wpvdbres == '1':
            cmseek.result("Vulnerability Count: " , str(len(result['vulnerabilities'])))
            cmseek.update_log('wp_vuln_count', str(len(result['vulnerabilities'])))
            cmseek.update_log('wpvulndb_url', "https://wpvulndb.com/api/v2/wordpresses/" + vfc)
            if len(result['vulnerabilities']) > 0:
                cmseek.success("Displaying all the vulnerabilities")
                for vuln in result['vulnerabilities']:
                    print("\n")
                    cmseek.result("Title: " , str(vuln['title']))
                    cmseek.result("Type: " , str(vuln['vuln_type']))
                    cmseek.result("Fixed In Version: " , str(vuln['fixed_in']))
                    cmseek.result("Link: " , "http://wpvulndb.com/vulnerabilities/" + str(vuln['id']))
                    strvuln = str(vuln)
                    if 'cve' in strvuln:
                        for ref in vuln['references']['cve']:
                            cmseek.result("CVE: ",  "http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-" + str(ref))

                    if 'exploitdb' in strvuln:
                        for ref in vuln['references']['exploitdb']:
                            cmseek.result("ExploitDB Link: ",  "http://www.exploit-db.com/exploits/" + str(ref))

                    if 'metasploit' in strvuln:
                        for ref in vuln['references']['metasploit']:
                            cmseek.result("Metasploit Module: ",  "http://www.metasploit.com/modules/" + str(ref))

                    if 'osvdb' in strvuln:
                        for ref in vuln['references']['osvdb']:
                            cmseek.result("OSVDB Link: ",  "http://osvdb.org/" + str(ref))

                    if 'secunia' in strvuln:
                        for ref in vuln['references']['secunia']:
                            cmseek.result("Secunia Advisory: ",  "http://secunia.com/advisories/" + str(ref))

                    if 'url' in strvuln:
                        for ref in vuln['references']['url']:
                            cmseek.result("Reference: ", str(ref))
            else:
                cmseek.warning('No vulnerabilities discovered in this version yet!')
            return
        else:
            cmseek.error("Could not look up version vulnerabilities")
            return


    return
