import sys
import os
import http.client
import urllib.request
import json
import importlib
from datetime import datetime

import deepscans.core as advanced # Deep scan and Version Detection functions
import cmseekdb.basic as cmseek # All the basic functions
import cmseekdb.sc as source # Contains function to detect cms from source code
import cmseekdb.header as header # Contains function to detect CMS from gathered http headers
import cmseekdb.cmss as cmsdb # Contains basic info about the CMSs

def main_proc(site,cua):
    cmseek.clearscreen()
    cmseek.banner("CMS Detection And Deep Scan")
    cmseek.info("Scanning Site: " + site)
    cmseek.statement("User Agent: " + cua)
    cmseek.statement("Collecting Headers and Page Source for Analysis")
    init_source = cmseek.getsource(site, cua)
    if init_source[0] != '1':
        cmseek.error("Aborting CMSeek! Couldn't connect to site \n    Error: %s" % init_source[1])
        return
    else:
        scode = init_source[1]
        headers = init_source[2]
        if site != init_source[3] and site + '/' != init_source[3]:
            cmseek.info('Target redirected to: ' + cmseek.bold + cmseek.fgreen + init_source[3] + cmseek.cln)
            follow_redir = input('[#] Set ' + cmseek.bold + cmseek.fgreen + init_source[3] + cmseek.cln + ' as target? (y/n): ')
            if follow_redir.lower() == 'y':
                site = init_source[3]
    cmseek.statement("Detection Started")
    cmseek.statement("Using headers to detect CMS (Stage 1 of 2)")
    c1 = header.check(headers)
    if c1[0] == "1":
        # Do this shit later
        cmseek.success("CMS Detected, CMS ID: \"%s\" - looking up database for CMS information" % c1[1])
        cmseek.update_log('detection_param','header') # update log
        cmseek.update_log('cms_id',c1[1]) # update log
        cka = getattr(cmsdb, c1[1])
        if cka['deeps'] != '1': # Deep Scan
            if cka['vd'] != '1': # Version Detection not available for the cms show basic stuff
                print('\n')
                cmseek.result('',"CMS Name: " + cmseek.bold + cmseek.fgreen + cka['name'] + cmseek.cln)
                cmseek.update_log('cms_name',cka['name']) # update log
                cmseek.result('',"CMS Link: " + cmseek.bold + cmseek.fgreen + cka['url'] + cmseek.cln)
                cmseek.update_log('cms_url',cka['url']) # update log
            else:
                cmseek.statement("CMS Version is detectable, detecting CMS Version")
                ### Detect version
                print('\n')
                cmseek.result('',"CMS Name: " + cmseek.bold + cmseek.fgreen + cka['name'] + cmseek.cln)
                cmseek.update_log('cms_name',cka['name']) # update log
                cmseek.result('',"CMS Link: " + cmseek.bold + cmseek.fgreen + cka['url'] + cmseek.cln)
                cmseek.update_log('cms_url',cka['url']) # update log
            # return
        else:
            advanced.start(c1[1], site, cua, '2', scode) ## The 2 suggests that generator check has not been performed
    else:
        cmseek.warning('No luck with headers... Continuing with source code')
        cmseek.statement("Checking for generator meta tag in source code")
        if 'Generator' in scode or 'generator' in scode:
            cmseek.success("Generator meta tag found.. Continuing with detection (2.1 of 2.2)")
            ga = "1" ## Generator tag found .. this will come in handy later to save us some milliseconds ;)
            c21 = source.generator(scode)
            if c21[0] == '1':
                cmseek.success("CMS Detected, CMS ID: \"%s\" - looking up database for CMS information" % c21[1])
                cmseek.update_log('detection_param','generator') # update log
                cmseek.update_log('cms_id',c21[1]) # update log
                cka = getattr(cmsdb, c21[1])
                if cka['deeps'] != '1': # Deep Scan not available
                    if cka['vd'] != '1': # Version Detection not available for the cms show basic stuff
                        print('\n')
                        cmseek.result('',"CMS Name: " + cmseek.bold + cmseek.fgreen + cka['name'] + cmseek.cln)
                        cmseek.update_log('cms_name',cka['name']) # update log
                        cmseek.result('',"CMS Link: " + cmseek.bold + cmseek.fgreen + cka['url'] + cmseek.cln)
                        cmseek.update_log('cms_url',cka['url']) # update log
                    else:
                        cmseek.statement("CMS Version is detectable, detecting CMS Version")
                        ### Detect version
                        print('\n')
                        cmseek.result('',"CMS Name: " + cmseek.bold + cmseek.fgreen + cka['name'] + cmseek.cln)
                        cmseek.update_log('cms_name',cka['name']) # update log
                        cmseek.result('',"CMS Link: " + cmseek.bold + cmseek.fgreen + cka['url'] + cmseek.cln)
                        cmseek.update_log('cms_url',cka['url']) # update log
                    # return
                else:
                    advanced.start(c21[1], site, cua, '1', scode)
            elif c21[0] == '2': # Empty Source code
                cmseek.error("Source code was empty... exiting CMSeek")
                # return
            else: ## CMS Detection unsuccessful via generator meta tag
                cmseek.warning('Could not detect CMS from the generator meta tag, (Procceeding with scan 2.2 of 2.2)')
                c22 = source.check(scode, site)
                if c22[0] == '1':
                    cmseek.success("CMS Detected, CMS ID: \"%s\" - looking up database for CMS information" % c22[1])
                    cmseek.update_log('detection_param','source') # update log
                    cmseek.update_log('cms_id',c22[1]) # update log
                    cka = getattr(cmsdb, c22[1])
                    if cka['deeps'] != '1': # Deep Scan not available
                        if cka['vd'] != '1': # Version Detection not available for the cms show basic stuff
                            print('\n')
                            cmseek.result('',"CMS Name: " + cmseek.bold + cmseek.fgreen + cka['name'] + cmseek.cln)
                            cmseek.update_log('cms_name',cka['name']) # update log
                            cmseek.result('',"CMS Link: " + cmseek.bold + cmseek.fgreen + cka['url'] + cmseek.cln)
                            cmseek.update_log('cms_url',cka['url']) # update log
                        else:
                            cmseek.statement("CMS Version is detectable, detecting CMS Version")
                            ### Detect version
                            print('\n')
                            cmseek.result('',"CMS Name: " + cmseek.bold + cmseek.fgreen + cka['name'] + cmseek.cln)
                            cmseek.update_log('cms_name',cka['name']) # update log
                            cmseek.result('',"CMS Link: " + cmseek.bold + cmseek.fgreen + cka['url'] + cmseek.cln)
                            cmseek.update_log('cms_url',cka['url']) # update log
                        return
                    else:
                        advanced.start(c22[1], site, cua, '1', scode)
                elif c22[0] == '2': # Empty Source code
                    cmseek.error("Source code was empty... exiting CMSeek")
                    return
                else:
                    cmseek.error("Couldn't detect cms... :( \n    Sorry master didn't mean to dissapoint but bye for now \n    Can't handle this much disappintment \n\n")
                    return
        else:
            cmseek.warning("Generator meta tag not found! (Procceeding with scan 2.2 of 2.2)")
            ga = '0' ## Generator meta tag not found as i freakin said earlier this will come in handy later
            c22 = source.check(scode, site)
            if c22[0] == '1':
                cmseek.success("CMS Detected, CMS ID: \"%s\" - looking up database for CMS information" % c22[1])
                cmseek.update_log('detection_param','source') # update log
                cmseek.update_log('cms_id',c22[1]) # update log
                cka = getattr(cmsdb, c22[1])
                if cka['deeps'] != '1': # Deep Scan not available
                    if cka['vd'] != '1': # Version Detection not available for the cms show basic stuff
                        print('\n')
                        cmseek.result('',"CMS Name: " + cmseek.bold + cmseek.fgreen + cka['name'] + cmseek.cln)
                        cmseek.update_log('cms_name',cka['name']) # update log
                        cmseek.result('',"CMS Link: " + cmseek.bold + cmseek.fgreen + cka['url'] + cmseek.cln)
                        cmseek.update_log('cms_url',cka['url']) # update log
                    else:
                        cmseek.statement("CMS Version is detectable, detecting CMS Version")
                        ### Detect version
                        print('\n')
                        cmseek.result('',"CMS Name: " + cmseek.bold + cmseek.fgreen + cka['name'] + cmseek.cln)
                        cmseek.update_log('cms_name',cka['name']) # update log
                        cmseek.result('',"CMS Link: " + cmseek.bold + cmseek.fgreen + cka['url'] + cmseek.cln)
                        cmseek.update_log('cms_url',cka['url']) # update log
                    return
                else:
                    advanced.start(c22[1], site, cua, '0', scode)
            elif c22[0] == '2': # Empty Source code
                cmseek.error("Source code was empty... exiting CMSeek")
                return
            else:
                cmseek.error("Couldn't detect cms... :( \n    Sorry master didn't mean to dissapoint but bye for now \n    Can't handle this much disappintment \n\n")
                return
