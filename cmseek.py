#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

## for people who don't bother reading the readme :/
if sys.version_info[0] < 3:
    print("\nPython3 is needed to run CMSeeK, Try \"python3 cmseek.py\" instead\n")
    sys.exit(2)

import os
import argparse
import json
import importlib

import cmseekdb.basic as cmseek # All the basic functions
import cmseekdb.core as core
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

parser = argparse.ArgumentParser(prog='cmseek.py',add_help=False)

parser.add_argument('-h', '--help', action="store_true")
parser.add_argument('-v', '--verbose', help="increase output verbosity", action="store_true")
parser.add_argument("--version", help="Show CMSeeK version", action="store_true")
parser.add_argument("--update", help="Update CMSeeK", action="store_true")
parser.add_argument('-r', "--random-agent", help="Use a random user agent", action="store_true")
parser.add_argument('--user-agent', help='Specify custom user agent')
parser.add_argument('-u', '--url', help='Target Url')
parser.add_argument('-l', '--list', help='path of the file containing list of sites for scan (comma separated)')
parser.add_argument('--clear-result', action='store_true')
args = parser.parse_args()

if args.clear_result:
    cmseek.clear_log()
if args.help:
    cmseek.help()
if args.verbose:
    cmseek.verbose = True
if args.update:
    cmseek.update()
if args.version:
    print('\n\n')
    cmseek.info("CMSeeK Version: " + cmseek.cmseek_version)
    cmseek.bye()
if args.user_agent is not None:
    cua = args.user_agent
elif args.random_agent is not None:
    cua = cmseek.randomua('random')
else:
    cua = None
if args.url is not None:
    s = args.url
    target = cmseek.process_url(s)
    if target != '0':
        if cua == None:
            cua = cmseek.randomua()
        core.main_proc(target,cua)
        cmseek.handle_quit()
elif args.list is not None:
    sites = args.list
    cmseek.clearscreen()
    cmseek.banner("CMS Detection And Deep Scan")
    sites_list = []
    try:
        ot = open(sites, 'r')
        file_contents = ot.read().replace('\n','')
        sites_list = file_contents.split(',')
    except FileNotFoundError:
        cmseek.error('Invalid path! CMSeeK is quitting')
        cmseek.bye()
    if sites_list != []:
        if cua == None:
            cua = cmseek.randomua()
        for s in sites_list:
            target = cmseek.process_url(s)
            if target != '0':
                core.main_proc(target,cua)
                cmseek.handle_quit(False)
                input('\n\n\tPress ' + cmseek.bold + cmseek.fgreen + '[ENTER]' + cmseek.cln + ' to continue') # maybe a fix? idk
            else:
                print('\n')
                cmseek.warning('Invalid URL: ' + cmseek.bold + s + cmseek.cln + ' Skipping to next')
        print('\n')
        cmseek.result('Finished Scanning all targets.. result has been saved under respective target directories','')
    else:
        cmseek.error("No url provided... CMSeeK is exiting")
    cmseek.bye()

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
print ("  [U]    Update CMSeeK")
print ("  [R]    Rebuild Cache (Use only when you add any custom module)")
print ("  [0]    Exit CMSeeK :( \n")

selone = input("Enter Your Desired Option: ").lower()
if selone == 'r':
    cmseek.update_brute_cache()
elif selone == 'u':
    cmseek.update()
elif selone == '0':
    cmseek.bye()
elif selone == "1":
    # There goes the cms detection thingy
    cmseek.clearscreen()
    cmseek.banner("CMS Detection And Deep Scan")
    site = cmseek.targetinp("") # Get The User input
    if cua == None:
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
        if cua == None:
            cua = cmseek.randomua()
        for s in sites_list:
            target = cmseek.process_url(s)
            if target != '0':
                core.main_proc(target,cua)
                cmseek.handle_quit(False)
                input('\n\n\tPress ' + cmseek.bold + cmseek.fgreen + '[ENTER]' + cmseek.cln + ' to continue') # maybe a fix? idk
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
        brute_list = sorted(brute_list)
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
