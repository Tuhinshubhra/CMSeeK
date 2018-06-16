#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import importlib

import cmseekdb.basic as cmseek # All the basic functions
import cmseekdb.core as core


### Operating System detection

if sys.platform == "Windows":
    cos = "win"
else:
    cos = "nwin"


################################
###      THE MAIN MENU       ###
################################
cmseek.clearscreen()
cmseek.banner("")
print (" Input    Description")
print ("=======  ==============================")
print ("  [1]    CMS detection and Deep scan")
print ("  [2]    Scan Multiple Sites")
print ("  [3]    Bruteforce CMSs")
print ("  [U]    Update Cache (in case you added any modules!)")
print ("  [0]    Exit CMSeeK :( \n")

selone = input("Enter Your Desired Option: ").lower()
if selone == 'u' or selone == 'U':
    cmseek.update_brute_cache()
elif selone == '0':
    cmseek.bye()
elif selone == "1":
    # There goes the cms detection thingy
    cmseek.clearscreen()
    cmseek.banner("CMS Detection And Deep Scan")
    site = cmseek.targetinp("") # Get The User input
    cua = cmseek.randomua()
    core.main_proc(site,cua)
    cmseek.handle_quit()

elif selone == '2':
    cmseek.clearscreen()
    cmseek.banner("CMS Detection And Deep Scan")
    sites_list = []
    sites = input('Enter comma separated urls(http://1.com,https://2.org) or enter path of file containing URLs (comma separated): ')
    if 'http' not in sites or '://' not in sites:
        cmseek.info('Treating input as path')
        try:
            ot = open(sites, 'r')
            file_contents = ot.read().replace('\n','')
            sites_list = file_contents.split(',')
        except FileNotFoundError:
            cmseek.error('Invalid path! CMSeeK is quitting')
            cmseek.bye()
    else:
        cmseek.info('Treating input as URL list')
        sites_list = sites.split(',')
    if sites_list != []:
        cua = cmseek.randomua()
        for s in sites_list:
            target = cmseek.process_url(s)
            if target != '0':
                core.main_proc(target,cua)
                cmseek.handle_quit(False)
            else:
                print('\n')
                cmseek.warning('Invalid URL: ' + cmseek.bold + s + cmseek.cln + ' Skipping to next')
        print('\n')
        cmseek.result('Finished Scanning all targets.. result has been saved under respective target directories','')
    else:
        cmseek.error("No url provided... CMSeeK is exiting")
    cmseek.bye()

elif selone == "3":
    cmseek.clearscreen()
    cmseek.banner("CMS Bruteforce Module")
    ## I think this is a modular approch
    brute_dir = os.getcwd() + "/cmsbrute"
    brute_cache = brute_dir + '/cache.json'
    if not os.path.isdir(brute_dir):
        cmseek.error("bruteforce directory missing! did you mess up with it? Anyways CMSeek is exiting")
        cmseek.bye()
    else:
        print ("[#] List of CMSs: \n")
        print (cmseek.bold)
        read_cache = open(brute_cache, 'r')
        b_cache = read_cache.read()
        cache = json.loads(b_cache)
        brute_list = []
        for c in cache:
            brute_list.append(c)
        for i,x in enumerate(brute_list):
            n = x
            mod = "cmsbrute." + x
            exec(n + " = importlib.import_module(mod)")
            print('['+ str(i) +'] ' + cache[x])
        print(cmseek.cln + '\n')
        cmstobrute = input('Select CMS: ')
        try:
            kek = brute_list[int(cmstobrute)]
            print(kek)
            cms_brute = getattr(locals().get(kek), 'start')
            cms_brute()
        except IndexError:
            cmseek.error('Invalid Input!')
else:
    cmseek.error("Invalid Input!")
    cmseek.bye()
