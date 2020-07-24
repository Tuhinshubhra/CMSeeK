#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra
# Thought this file was getting quite bloated so refectored it

import errno
import sys
import os
import random
import shutil
import signal
import subprocess
import urllib.request
from http.cookiejar import CookieJar
import json
from datetime import datetime
import time
import re
from cmseekdb.getsource import *
from cmseekdb.config import *

cmseek_dir = os.path.dirname(os.path.abspath(__file__)).replace('cmseekdb','')[:-1]    
total_requests = 0
cstart = time.time()
redirect_conf = '0' # 0 = prompt for redirect, 1 = follow redirect, 2 = do not follow any redirect
batch_mode = False # When set to true cmseek won't ask you to press enter after every site in a list is scanned
ignore_cms = [] # add cms id that you want to skip
strict_cms = [] # add cms ids that you want to detect.. no other cmses will be detected when any id is provided.
report_index = {} # Contains previous scan results
skip_scanned = False # When set to true CMSeeK witll ignore target whose CMS had been previously detected!
light_scan = False # When enabled, we don't perform deep-scan only detect CMS and version.
only_cms = False # When enabled, we just detect the CMS no version or deepscan is performed.

# all the color codes goes here
white = "\033[97m"
black = "\033[30m\033[1m"
yellow = "\033[93m"
orange = "\033[38;5;208m"
blue   = "\033[34m"
lblue  = "\033[36m"
cln    = "\033[0m"
green  = "\033[92m"
fgreen = "\033[32m"
red    = "\033[91m"
magenta = "\033[35m"
blackbg = "\033[100m"
whitebg = "\033[107m"
bluebg = "\033[44m"
lbluebg = "\033[106m"
greenbg = "\033[42m"
lgreenbg = "\033[102m"
yellowbg = "\033[43m"
lyellowbg = "\033[103m"
violetbg = "\033[48;5;129m"
redbg = "\033[101m";
grey = "\033[37m";
cyan = "\033[36m";
bold   = "\033[1m";

# access_directory
if access_directory == "" or not os.path.exists(access_directory):
    # no custom path provided or the path provided is wrong!
    # show a warning if the case is wrong path
    if not os.path.exists(access_directory) and access_directory != "":
        if verbose:
            print(bold + yellow + "[!] " + cln + "Invalid access_directory! falling back to default")

    if os.access(cmseek_dir, os.W_OK):
        # use the parent CMSeeK directory if it is writeable
        access_directory = cmseek_dir
    else:
        if cmseek_dir == os.getcwd():
            # current directory and cmseek directory are same and write access not available. show error if --batch is not used
            if not batch_mode:
                input(bold + red + "[x] " + "No write access in current directory, Reports will not be saved! [ENTER to continue]" + cln)

            access_directory = cmseek_dir
        else:
            # current directory is different
            access_directory = os.getcwd()

def banner (txt):
    # The sexy banner!!!
    global cmseek_version
    print(bold + fgreen + """
{1} {5}___ _  _ {1}__{5}__ ____ {1}____{5} _  {1}_{5}
|    |{1}\/{5}| {1}[{5}__  {1}|{5}___ |{1}___{5} |{1}_{5}/  {0}by {4}@r3dhax0r{5}
{1}|{5}_{1}__{5} |  | ___{1}|{5} |{1}___{5} {1}|{5}___ {1}|{5} \{1}_{5} {2}Version {3}{1} K-RONA
""".format(orange, lblue, yellow, cmseek_version, red, white))
    if txt != "":
        print(whitebg + black + bold)
        print(" [+]  " + txt + "  [+] " + cln)
    else:
        print(cln + bold + lbluebg + black + " Author: " + cln + bold + " https://twitter.com/r3dhax0r" + blackbg + white + "\n GitHub: " + cln + bold + " https://github.com/Tuhinshubhra \n" + cln + '\n')
    print(cln)
    return

def help():
    # The help screen
    print(
    """
CMSeeK Version {0}
Github: {4}
Coded By:{1}{3} @r3dhax0r {2}

USAGE:
       python3 cmseek.py (for guided scanning) OR
       python3 cmseek.py [OPTIONS] <Target Specification>

SPECIFING TARGET:
      -u URL, --url URL            Target Url
      -l LIST, --list LIST         Path of the file containing list of sites
                                   for multi-site scan (comma separated)

MANIPULATING SCAN:
      -i cms, --ignore--cms cms    Specify which CMS IDs to skip in order to
                                   avoid flase positive. separated by comma ","

      --strict-cms cms             Checks target against a list of provided
                                   CMS IDs. separated by comma ","

      --skip-scanned               Skips target if it's CMS was previously detected.

      --light-scan                 Skips Deep Scan. Does CMS and version detection only.

      -o, --only-cms               Only detect CMS, ignore deep scan and version detection.

RE-DIRECT:
      --follow-redirect            Follows all/any redirect(s)
      --no-redirect                Skips all redirects and tests the input target(s)

USER AGENT:
      -r, --random-agent           Use a random user agent
      --googlebot                  Use Google bot user agent
      --user-agent USER_AGENT      Specify a custom user agent

OUTPUT:
      -v, --verbose                Increase output verbosity

VERSION & UPDATING:
      --update                     Update CMSeeK (Requires git)
      --version                    Show CMSeeK version and exit

HELP & MISCELLANEOUS:
      -h, --help                   Show this help message and exit
      --clear-result               Delete all the scan result
      --batch                      Never ask you to press enter after every site in a list is scanned

EXAMPLE USAGE:
      python3 cmseek.py -u example.com                           # Scan example.com
      python3 cmseek.py -l /home/user/target.txt                 # Scan the sites specified in target.txt (comma separated)
      python3 cmseek.py -u example.com --user-agent Mozilla 5.0  # Scan example.com using custom user-Agent Mozilla is 5.0 used here
      python3 cmseek.py -u example.com --random-agent            # Scan example.com using a random user-Agent
      python3 cmseek.py -v -u example.com                        # enabling verbose output while scanning example.com

    """.format(cmseek_version,red, cln, bold, GIT_URL))
    bye()

def signal_handler(signal, frame):
    # Handle Ctrl+c
    handle_quit()

signal.signal(signal.SIGINT, signal_handler)

def clearscreen():
    if os.name == 'nt':
        os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        os.system('clear')

def bye():
    bye_dict = ["adios","adieu","addio","adeus","aloha","arrivederci","auf Wiedersehen","au revoir","sayonara","shalom","totsiens","vale","zaijian","Aabar dekha hobey","Fir milenge","Annyeong", "Ja mata ne", "До Встречи"]
    this_time = random.choice(bye_dict)
    print('\n' + bold + red + ' CMSeeK says ~ ' + this_time + cln)
    quit()

def statement(msg):
    # Print only if verbose
    global verbose
    if verbose == True:
        print("[+] "  + msg)

def error(msg):
    print(bold + red + "[x] " + msg + cln) # switched to x from ❌ ..

def warning(msg):
    print(bold + yellow + "[!] " + cln + msg)

def info(msg):
    print(bold + lblue + "[i] " + cln + msg)

def success(msg):
    print(bold + fgreen + "[*] " + cln + msg)

def result(stm, msg):
    try: print(bold + fgreen + "[✔] " + stm + cln + msg)
    except UnicodeEncodeError:
        print(bold + fgreen + "[>] " + stm + cln + msg)

def process_url(target):
    # Used to format the url for multiple site scan
    # 0 = invalid URL
    if target == "":
        return '0'
    elif "://" in target and "http" in target:
        target = target
        # if not target.endswith('/'):
        #     if '.php' in target or '.html' in target or '.asp' in target or '.aspx' in target or '.htm' in target or '.py' in target or '.pl' in target:
        #         target = target
        #     else:
        #         target = target + '/'
    else:
        target = 'http://' + target
        # if not target.endswith('/'):
        #     if '.php' in target or '.html' in target or '.asp' in target or '.aspx' in target or '.htm' in target or '.py' in target or '.pl' in target:
        #         target = target
        #     else:
        #         target = target + '/'
    init_result_dir(target)
    update_log('url', str(target))
    return target


def targetinp(iserr):
    # site url validator and stuff...
    if iserr != "":
        target = input(iserr + " : " + cln).lower()
    else:
        target = input("Enter target site (https://example.tld): ").lower()
    if "://" in target and "http" in target:
        if not target.endswith('/'):
            target = target + '/'
        init_result_dir(target)
        update_log('url', str(target))
        return target
    else:
        return targetinp(red + "Invalid URL format, correct format (https://example.tld)")

def init_result_dir(url):
    ### initiate log directory and stuffs
    ## trim the url to use as a suitable directory Name
    if "http://" in url:
        url = url.replace('http://', '')
    elif "https://" in url:
        url = url.replace('https://', '')
    else:
        print('wtf man did you forget to use the targetinp function!!!')
    if url.endswith('/'):
        # This seemed preety ugly to me tbh
        url = list(url)
        url[-1] = ""
        url = "".join(url)
    tor = {'/','!','?','#','@','&','%','\\','*', ':'}
    for r in tor:
        url = url.replace(r, '_')

    
    global access_directory
    result_dir = os.path.join(access_directory, "Result", url)
    json_log = os.path.join(result_dir, 'cms.json')

    ## check if the log directory exist
    if not os.path.isdir(result_dir):
        try:
            os.makedirs(result_dir)
            f = open(json_log,"w+")
            f.write("")
            f.close()
            # print('directory created')
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    else:
        # Directory exists, check for json log
        if not os.path.isfile(json_log):
            f = open(json_log,"w+")
            f.write("")
            f.close()
        else:
            # read log and save it to a variable
            f = open(json_log,"r")
            log_cont = f.read()
            if log_cont != "":
                try:
                    global log
                    log = log_cont
                except ValueError:
                    # invalid json file... clear it i guess
                    f = open(json_log,"w+")
                    f.write("")
                    f.close()
    global log_dir
    log_dir = result_dir
    update_log('last_scanned', str(datetime.now()))


def update_log(key, value, _isString=True):
    if key != "":
        global log
        a = json.loads(log)
        a[key] = str(value) if _isString else value
        log = json.JSONEncoder().encode(a)

def clear_log():
    # Clear Result directory
    global access_directory
    resdir = os.path.join(access_directory, 'Result')
    if os.path.isdir(resdir):
        shutil.rmtree(resdir)
        os.makedirs(resdir)
        success('Result directory cleared successfully!')
        bye()
    else:
        warning('Results directory not found!')
        bye()

def handle_quit(end_prog = True):
    # in case of unwanted exit this function should take care of writing the json log
    global log_dir
    if log_dir != "":
        log_file = os.path.join(log_dir, 'cms.json')
        # print(log_file)
        global log
        f = open(log_file,"w+")
        json_l = json.loads(log)
        log_to_write = json.dumps(json_l, sort_keys=True, indent=4)
        f.write(log_to_write)
        # print('written: ' + log)
        f.close()
        print('\n')
        # info('Log saved in: ' + fgreen + bold + log_file + cln)
    if end_prog == True:
        bye()
    else:
        log = '{"url":"","last_scanned":"","detection_param":"","cms_id":"","cms_name":"","cms_url":""}'

def update_brute_cache():
    clearscreen()
    banner("Updating Bruteforce Cache")
    global cmseek_dir
    brute_dir = os.path.join(cmseek_dir, "cmsbrute")
    brute_cache = os.path.join(brute_dir, 'cache.json')
    cache_json = {}
    if not os.path.isdir(brute_dir):
        try:
            error('CMSeeK could not find the bruteforce directory, Creating Brute directory')
            os.makedirs(brute_dir)
            info('Bruteforce directory created, add some modules from: https://github.com/Tuhinshubhra/cmseek')
            bye()
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    py_files = os.listdir(brute_dir)
    modules = []
    modulen = []
    for f in py_files:
        if f.endswith('.py') and f != '__init__.py':
            fo = open(os.path.join(brute_dir, f), 'r')
            mod_cnt = fo.read()
            if 'cmseekbruteforcemodule' in mod_cnt and 'Bruteforce module' in mod_cnt:
                n = []
                n = re.findall(r'\# (.*?) Bruteforce module', mod_cnt)
                if n != [] and n[0] != "":
                    modules.append(f)
                    modulen.append(n[0])
    if not modules == [] and modulen != []:
        info('Found ' + str(len(modules)) + ' modules.. Writting cache')
        for index,module in enumerate(modules):
            module = module.replace('.py','')
            cache_json[module] = modulen[index]
        tuh = open(brute_cache, 'w+')
        tuh.write(json.dumps(cache_json))
        tuh.close()
        success('The following modules has been added to the cache: \n')
        for ma in cache_json:
            print('> ' + bold + ma + '.py ' + cln + '--->   ' + bold + cache_json[ma] + cln + ' Bruteforce Module')
        print('\n')
        result('Cache Updated! Enjoy CMSeeK with new modules ;)','')
    else:
        warning('Could not find any modules! either there are no modules or someone messed with em!')
    bye()

def update():
    # Check For Update
    clearscreen()
    banner("Update Menu")
    global cmseek_version
    my_version = int(cmseek_version.replace('.',''))
    info("Checking for updates")
    get_version = getsource('https://raw.githubusercontent.com/Tuhinshubhra/CMSeeK/master/current_version',randomua('generate'))
    if get_version[0] != '1':
        error('Could not get latest version, Error: ' + get_version[1])
        bye()
    else:
        latest_version = get_version[1].replace('\n','')
        serv_version = int(latest_version.replace('.',''))
        info("CMSeeK Version: " + cmseek_version)
        success("Latest Version: " + latest_version)
        if my_version > serv_version:
            print('\n')
            error("Either you or me (The Developer) messed things up.\n" + cln + "[↓] Download the proper version from: " + fgreen + bold + GIT_URL)
        elif my_version == serv_version:
            print('\n')
            result("CMSeeK is up to date, Thanks for checking update tho.. It's a good practise",'')
        else:
            print('\n')
            #success("Update available!")
            success("Update available!")
            update_me = input("[#] Do you want to update now? (y/n): ")
            if update_me.lower() == 'y':
                print(bold + fgreen + "[↓]" + cln + " Downloading Update...")
                succes = False
                try:
                    global cmseek_dir
                    lock_file = os.path.join(cmseek_dir, "/.git/index.lock")
                    if os.path.isfile(lock_file):
                        statement("Removing index.lock file from .git directory")
                        # Solve the index.lock issue
                        os.remove(lock_file)
                    subprocess.run(("git checkout . && git pull %s HEAD") % GIT_URL, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    #os.system("git checkout . && git pull %s HEAD" % GIT_URL)
                    vt = open('current_version', 'r')
                    v_test = int(vt.read().replace('\n','').replace('.',''))
                    # print(v_test)
                    # print(serv_version)
                    if v_test == serv_version:
                        # Check if update successful
                        succes = True
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    raise
                    error("Automatic Update Failed! Pleae download manually from: " + cln + GIT_URL)
                if succes == True:
                    result("CMSeeK Updated To Latest Version! Enjoy", "")
                else:
                    warning(bold + orange + "Update might be not successful.. Download manually from: " + cln + GIT_URL)
            else:
                print('\n')
                warning("Automatic Update Terminated!")
                info("Update Manually from: " + fgreen + bold + GIT_URL + cln)
        bye()


def savebrute(url,adminurl,username,password):
    # write the results to a result file
    if url != "" and adminurl != "" and username != "" and password != "":
        global log_dir
        brute_file = os.path.join(log_dir, 'bruteforce_result_' + username + '_.txt')
        old_file = os.path.join(log_dir, 'bruteforce_result_' + username + '_.old.txt')
        brute_result = "### CMSeeK Bruteforce Result\n\n\nSite: " + url + "\n\nLogin URL: " + adminurl + "\n\nUsername: " + username + "\n\nPassword: " + password
        print('\n\n') # Pretty sloppy move there ;-;
        if not os.path.isfile(brute_file):
            # No previous bruteforce result file Found
            f = open(brute_file, 'w+')
            f.write(brute_result)
            f.close()
            success('Credentials stored at: ' + bold + brute_file + cln)
        else:
            os.rename(brute_file, old_file)
            info("Old result file found and moved to: " + old_file)
            f = open(brute_file, 'w+')
            f.write(brute_result)
            f.close()
            success('New credentials stored at: ' + bold + brute_file + cln)


def getsource(url, ua):
    '''
    (url, useragent)
    return type: [(0/1/2), (error/source code/error), (empty/http headers/empty)]
    '''
    raw_source = getrawsource(url, ua)
    global total_requests
    total_requests += 1
    if 'Please prove that you are human' in raw_source[1] or '?ckattempt=' in raw_source[1]:
        warning('Browser validation detected.. trying to evade...')
        ## This can be evaded by using googlebot as user agent so let's do that
        raw_source = getrawsource(url, 'Googlebot/2.1 (+http://www.google.com/bot.html)')
        ## final check..
        if '?ckattempt=' in raw_source[1]:
            error('Failed to evade Browser validation, detection results might not be accurate!')
            return raw_source
        else:
            success('Browser validation successfully evaded..')
            return raw_source

    if 'src="/aes.js"' in raw_source[1] and '?i=1' in raw_source[1]:
        warning('Browser validation detected.. trying to evade...')
        ## This can be evaded by using googlebot as user agent so let's do that
        raw_source = getrawsource(url, 'Googlebot/2.1 (+http://www.google.com/bot.html)')
        ## final check..
        if '?i=' in raw_source[1] and 'src="/aes.js"' in raw_source[1]:
            error('Failed to evade Browser validation, detection results might not be accurate!')
            return raw_source
        else:
            success('Browser validation successfully evaded..')
            return raw_source
    if raw_source[2] == '403':
        if 'Abuse: Your connection is not welcome due to: Bot UA' in raw_source[3] or 'Warning: 199' in raw_source[3]:
            warning('UA validation detected.. trying to evade...')
            raw_source = getrawsource(url, 'Googlebot/2.1 (+http://www.google.com/bot.html)')
            if 'Bot UA' in raw_source[2] and 'Warning: 199' in raw_source[2]:
                error('Failed to evade UA validation, detection results might not be accurate!')
                return raw_source
            else:
                success('UA validation successfully evaded..')
                return raw_source

    return raw_source

def check_url(url,ua):
    global total_requests
    total_requests += 1
    request = urllib.request.Request(url)
    request.add_header('User-Agent', ua)
    request.get_method = lambda: 'HEAD'
    try:
        urllib.request.urlopen(request)
        return '1'
    except urllib.request.HTTPError:
        return '0'

def wpbrutesrc(url, user, pwd):
    redirecto = url + '/wp-admin/'
    url = url + '/wp-login.php'
    ua = randomua('generatenewuaeverytimetobesafeiguess')
    try:
        ckreq = urllib.request.Request(
        url,
        data=urllib.parse.urlencode({'log' : user, 'pwd' : pwd, 'wp-submit' : 'Log In', 'redirect_to' : redirecto}).encode("utf-8"),
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

def randomua(rnd = None): # Randomized or User defined useragent
    a = ["Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5","Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1","Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)","Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1","Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1","Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120403211507 Firefox/12.0","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1","Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)","Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/6.0)","Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00","Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5","Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13","Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1","Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418.8 (KHTML, like Gecko) Safari/419.3","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.20 Safari/535.1","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Ubuntu/10.10 Chromium/12.0.703.0 Chrome/12.0.703.0 Safari/534.24","Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.9) Gecko/20100915 Gentoo Firefox/3.6.9","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.16) Gecko/20120421 Gecko Firefox/11.0","Mozilla/5.0 (X11; Linux i686; rv:12.0) Gecko/20100101 Firefox/12.0","Opera/9.80 (X11; Linux x86_64; U; pl) Presto/2.7.62 Version/11.00","Mozilla/5.0 (X11; U; Linux x86_64; us; rv:1.9.1.19) Gecko/20110430 shadowfox/7.0 (like Firefox/7.0)"]

    if rnd == None:
        b = input("Enter custom UserAgent or simply press enter to use a random one: ")
        if b == "":
            b = random.choice(a)
        else:
            pass
    else:
        b = random.choice(a)

    return b
