#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

import cmseekdb.basic as cmseek ## Good old module
import re ## Comes in handy while detecting version
import json ## For parsing the wpvulndb result
import threading

wpparamuser = []

def wpauthorenum(ua, url, param):
    ## WordPress function for Collecting usernames from author Parameter
    ## Had to create a different function to avoid some pickle issues
    global wpparamuser
    param = param + 1
    i = str(param)
    # cmseek.statement('Checking for ?author=' + i) # Looks Ugly.. enable if you want over verbose result
    authorsrc = cmseek.getsource(url + '/?author=' + i, ua)
    if authorsrc[0] == '1' and '/author/' in authorsrc[3]: ## Detection using the url redirection
        author = re.findall(r'/author/(.*?)/', str(authorsrc[3]))
        if author != []:
            cmseek.success('Found user from redirection: ' + cmseek.fgreen + cmseek.bold + author[0] + cmseek.cln)
            wpparamuser.append(author[0])
    elif authorsrc[0] == '1' and '/author/' in authorsrc[1]:
        author = re.findall(r'/author/(.*?)/', str(authorsrc[1]))
        if author != []:
            cmseek.success('Found user from source code: ' + cmseek.fgreen + cmseek.bold + author[0] + cmseek.cln)
            wpparamuser.append(author[0])

def start(id, url, ua, ga, source):
    cmseek.info("Starting Username Harvest")

    # User enumertion via site's json api
    cmseek.info('Harvesting usernames from wp-json api')
    wpjsonuser = []
    wpjsonsrc = cmseek.getsource(url + '/wp-json/wp/v2/users', ua)
    if wpjsonsrc[0] != "1" or 'slug' not in wpjsonsrc[1]:
        cmseek.warning("Json api method failed trying with next")
    else:
        try:
            for user in json.loads(wpjsonsrc[1]):
                wpjsonuser.append(user['slug'])
                cmseek.success("Found user from wp-json : " + cmseek.fgreen + cmseek.bold + user['slug'] + cmseek.cln)
        except:
            cmseek.warning("Failed to parse json")
    # user enumertion vua jetpack api
    cmseek.info('Harvesting usernames from jetpack public api')
    jpapiuser = []
    strippedurl = url.replace('http://','')
    strippedurl = strippedurl.replace('https://', '') # Pretty sure it is an ugly solution but oh well
    jpapisrc = cmseek.getsource('https://public-api.wordpress.com/rest/v1.1/sites/' + strippedurl + '/posts?number=100&pretty=true&fields=author', ua)
    if jpapisrc[0] != '1' or 'login' not in jpapisrc[1]:
        cmseek.warning('No results from jetpack api... maybe the site doesn\'t use jetpack')
    else:
        for user in json.loads(jpapisrc[1])['posts']:
            if user['author']['login'] not in str(jpapiuser):
                jpapiuser.append(user['author']['login'])
                cmseek.success("Found user from Jetpack api : " + cmseek.fgreen + cmseek.bold + user['author']['login'] + cmseek.cln)
        jpapiuser = list(set(usr.strip() for usr in jpapiuser)) # Removing duplicate usernames

    # the regular way of checking vua user Parameter -- For now just check upto 20 ids
    cmseek.info('Harvesting usernames from wordpress author Parameter')
    global wpparamuser
    wpparamuser = []
    usrrange = range(31) # ain't it Obvious
    threads = [threading.Thread(target=wpauthorenum, args=(ua,url,r)) for r in usrrange]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    # Combine all the usernames that we collected
    usernames = set(wpjsonuser+jpapiuser+wpparamuser)
    if len(usernames) > 0:
        usernamesgen = '1' # Some usernames were harvested
        if len(usernames) == 1:
            cmseek.success(cmseek.bold + cmseek.fgreen + str(len(usernames)) + " Usernames" + " was enumerated"  + cmseek.cln)
        else:
            cmseek.success(cmseek.bold + cmseek.fgreen + str(len(usernames)) + " Usernames" + " were enumerated"  + cmseek.cln)
    else:
        usernamesgen = '0' # Failure
        cmseek.warning("Couldn't enumerate usernames :( ")

    return [usernamesgen, usernames]
