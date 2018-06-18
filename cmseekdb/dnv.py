### Version Detection and deep scan shits goes Here
import cmseekdb.basic as cmseek ## Good old module
import re ## Comes in handy while detecting version
import json ## For parsing the wpvulndb result
import multiprocessing ## Let's speed things up a lil bit (actually a hell lot faster) shell we?
from functools import partial ## needed somewhere :/

def version(id, url):
    ## Do the shits later
    print("version detection mate")
    return

def wpauthorenum(ua, url, param):
    ## WordPress function for Collecting usernames from author Parameter
    ## Had to create a different function to avoid some pickle issues
    param = param + 1
    i = str(param)
    # cmseek.statement('Checking for ?author=' + i) # Looks Ugly.. enable if you want over verbose result
    authorsrc = cmseek.getsource(url + '/?author=' + i, ua)
    if authorsrc[0] == '1' and '/author/' in authorsrc[3]: ## Detection using the url redirection
        author = re.findall(r'/author/(.*?)/', str(authorsrc[3]))
        if author != []:
            cmseek.success('Found user from redirection: ' + cmseek.bold + author[0] + cmseek.cln)
            return author[0]
    elif authorsrc[0] == '1' and '/author/' in authorsrc[1]:
        author = re.findall(r'/author/(.*?)/', str(authorsrc[1]))
        if author != []:
            cmseek.success('Found user from source code: ' + cmseek.bold + author[0] + cmseek.cln)
            return author[0]


def deep(id, url, ua, ga, source): ## ({ID of the cms}, {url of target}, {User Agent}, {is Generator Meta tag available [0/1]}, {Source code})
    ## Do shits later [update from later: i forgot what shit i had to do ;___;]
    if id == "wp":
        cmseek.statement('Starting WordPress DeepScan')
        # Version detection
        version = '0'
        cmseek.statement('Detecting Version and vulnerabilities')
        if ga == '1' or ga == '2' or ga == '3': ## something good was going to happen but my sleep messed it up TODO: will fix it later
            cmseek.statement('Generator Tag Available... Trying version detection using generator meta tag')
            rr = re.findall(r'<meta name=\"generator\" content=\"WordPress (.*?)\"', source)
            if rr != []:
                version = rr[0]
                cmseek.success("Version Detected, WordPress Version %s" % version)
            else:
                cmseek.warning("Generator tag was a big failure.. looking up /feed/")
                fs = cmseek.getsource(url + '/feed/', ua)
                if fs[0] != '1': # Something messed up real bad
                    cmseek.warning("Couldn't get feed source code, Error: %s" % fs[1])
                else:
                    fv = re.findall(r'<generator>https://wordpress.org/\?v=(.*?)</generator>', fs[1])
                    if fv != []: # Not empty good news xD
                        version = fv[0]
                        cmseek.success("Version Detected, WordPress Version %s" % version)
                    else:
                        cmseek.warning("Well even feed was a failure... let's lookup wp-links-opml then")
                        opmls = cmseek.getsource(url + '/wp-links-opml.php', ua)
                        if opmls[0] != '1': # Something messed up real bad
                            cmseek.warning("Couldn't get wp-links-links source code, Error: %s" % opmls[1])
                        else:
                            fv = re.findall(r'generator=\"wordpress/(.*?)\"', opmls[1])
                            if fv != []: # Not empty good news xD || you can guess it's copied right?
                                version = fv[0]
                                cmseek.success("Version Detected, WordPress Version %s" % version)
                            else:
                                ## new version detection methods will be added in the future updates
                                cmseek.error("Couldn't Detect Version :( Sorry Master")
                                version = '0'

            ## Check for minor stuffs like licesnse readme and some open directory checks
            cmseek.statement("Initiating open directory and files check")

            ## Readme.html
            readmesrc = cmseek.getsource(url + '/readme.html', ua)
            if readmesrc[0] != '1': ## something went wrong while getting the source codes
                cmseek.warning("Couldn't get readme file's source code most likely it's not present")
                readmefile = '0' # Error Getting Readme file
            elif 'Welcome. WordPress is a very special project to me.' in readmesrc[1]:
                readmefile = '1' # Readme file present
            else:
                readmefile = '2' # Readme file found but most likely it's not of wordpress

            ## license.txt
            licsrc = cmseek.getsource(url + '/license.txt', ua)
            if licsrc[0] != '1':
                cmseek.warning('license file not found')
                licfile = '0'
            elif 'WordPress - Web publishing software' in licsrc[1]:
                licfile = '1'
            else:
                licfile = '2'

            ## wp-content/uploads/ folder
            wpupsrc = cmseek.getsource(url + '/wp-content/uploads/', ua)
            if wpupsrc[0] != '1':
                wpupdir = '0'
            elif 'Index of /wp-content/uploads' in wpupsrc[1]:
                wpupdir = '1'
            else:
                wpupdir = '2'

            ## xmlrpc
            xmlrpcsrc = cmseek.getsource(url + '/xmlrpc.php', ua)
            if xmlrpcsrc[0] != '1':
                cmseek.warning('XML-RPC interface not available')
                xmlrpc = '0'
            elif 'XML-RPC server accepts POST requests only.' in xmlrpcsrc[1]:
                xmlrpc = '1'
            else:
                xmlrpc = '2'

            ## User enumeration
            cmseek.info("Starting Username Harvest")

            # User enumertion via site's json api
            cmseek.info('Harvesting usernames from wp-json api')
            wpjsonuser = []
            wpjsonsrc = cmseek.getsource(url + '/wp-json/wp/v2/users', ua)
            if wpjsonsrc[0] != "1" or 'slug' not in wpjsonsrc[1]:
                cmseek.warning("Json api method failed trying with next")
            else:
                for user in json.loads(wpjsonsrc[1]):
                    wpjsonuser.append(user['slug'])
                    cmseek.success("Found User: %s" % user['slug'])

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
                    jpapiuser.append(user['author']['login'])
                    cmseek.success("Found User: %s" % user['author']['login'])
                jpapiuser = list(set(usr.strip() for usr in jpapiuser)) # Removing duplicate usernames

            # the regular way of checking vua user Parameter -- For now just check upto 20 ids
            cmseek.info('Harvesting usernames from wordpress author Parameter')
            wpparamuser = []
            usrrange = range(31)
            pool = multiprocessing.Pool()
            prepareenum = partial(wpauthorenum, ua, url)
            res  = pool.map(prepareenum,usrrange)
            for r in res:
                if r != None:
                    wpparamuser.append(r)

            # Combine all the usernames that we collected
            usernames = set(wpjsonuser+jpapiuser+wpparamuser)
            if len(usernames) > 0:
                usernamesgen = '1' # Some usernames were harvested
                cmseek.success(cmseek.bold + str(len(usernames)) + " Usernames"  + cmseek.cln + " was / were enumerated")
            else:
                usernamesgen = '0' # Failure
                cmseek.warning("Couldn't enumerate usernames :( ")
            ## Version Vulnerability Detection
            if version == "0":
                cmseek.warning("Skipping version vulnerability scan as WordPress Version wasn't detected")
                wpvdbres = '0' # fix for issue #3
            else: ## So we have a version let's scan for vulnerabilities
                cmseek.info("Checking version vulnerabilities [props to wpvulndb for their awesome api ;)]")
                vfc = version.replace('.','') # NOT IMPORTANT: vfc = version for check well we have to kill all the .s in the version for looking it up on wpvulndb.. kinda weird if you ask me
                ws = cmseek.getsource("https://wpvulndb.com/api/v2/wordpresses/" + vfc, ua)
                print(ws[0])
                if ws[0] == "1":
                    # wjson = json.loads(ws[1]) + vfd + "['release_date']"
                    wpvdbres = '1' ## We have the wpvulndb results
                    result = json.loads(ws[1])[version]
                else:
                    wpvdbres = '0'
                    cmseek.error('Error Retriving data from wpvulndb')

        ### Deep Scan Results comes here
        cmseek.clearscreen()
        cmseek.banner("Deep Scan Results")
        cmseek.result("Detected CMS: ", 'WordPress')
        cmseek.update_log('cms_name','WordPress') # update log
        cmseek.result("CMS URL: ", "https://wordpress.org")
        cmseek.update_log('cms_url', "https://wordpress.org") # update log
        if version != '0':
            cmseek.result("Version: ", version)
            cmseek.update_log('wp_version', version)
        if wpvdbres == '1':
            cmseek.result("Changelog URL: " , str(result['changelog_url']))
            cmseek.update_log('wp_changelog_file',str(result['changelog_url']))
        if readmefile == '1':
            cmseek.result("Readme file found: ", url + '/readme.html')
            cmseek.update_log('wp_readme_file',url + '/readme.html')
        if licfile == '1':
            cmseek.result("License file found: ", url + '/license.txt')
        if wpupdir == '1':
            cmseek.result("Uploads directory has listing enabled: ", url + '/wp-content/uploads')
            cmseek.update_log('wp_uploads_directory',url + '/wp-content/uploads')
        if xmlrpc == '1':
            cmseek.result("XML-RPC interface available: ", url + '/xmlrpc.php')
            cmseek.update_log('wp_uploads_directory', url + '/xmlrpc.php')
        if usernamesgen == '1':
            cmseek.result("Usernames Harvested: ",'')
            wpunames = ""
            for u in usernames:
                wpunames = wpunames + u + ","
                cmseek.success(cmseek.bold + u + cmseek.cln)
            print('\n')
            cmseek.update_log('wp_users', wpunames)
        if wpvdbres == '1':
            cmseek.result("Vulnerability Count: " , str(len(result['vulnerabilities'])))
            cmseek.update_log('wp_vuln_count', str(len(result['vulnerabilities'])))
            cmseek.update_log('wpvulndb_url', "https://wpvulndb.com/api/v2/wordpresses/" + vfc)
            if len(result['vulnerabilities']) > 0:
                cmseek.success("Displaying all the vulnerabilities")
                for vuln in result['vulnerabilities']:
                    print("\n")
                    cmseek.result("Vulnerability Title: " , str(vuln['title']))
                    cmseek.result("Vulnerability Type: " , str(vuln['vuln_type']))
                    cmseek.result("Fixed In Version: " , str(vuln['fixed_in']))
                    cmseek.result("Vulnerability Link: " , "http://wpvulndb.com/vulnerabilities/" + str(vuln['id']))
                    strvuln = str(vuln)
                    if 'cve' in strvuln:
                        for ref in vuln['references']['cve']:
                            cmseek.result("Vulnerability CVE: ",  "http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-" + str(ref))

                    if 'exploitdb' in strvuln:
                        for ref in vuln['references']['exploitdb']:
                            cmseek.result("ExploitDB Link: ",  "http://www.exploit-db.com/exploits/" + str(ref))

                    if 'metasploit' in strvuln:
                        for ref in vuln['references']['metasploit']:
                            cmseek.result("Metasploit Module: ",  "http://www.metasploit.com/modules/" + str(ref))

                    if 'osvdb' in strvuln:
                        for ref in vuln['references']['osvdb']:
                            cmseek.result("OSVDB Link: ",  "http://osvdb.org/" + str(ref))

                    if 'secunia' in strvuln:
                        for ref in vuln['references']['secunia']:
                            cmseek.result("Secunia Advisory: ",  "http://secunia.com/advisories/" + str(ref))

                    if 'url' in strvuln:
                        for ref in vuln['references']['url']:
                            cmseek.result("Vulnerability Reference: ", str(ref))
            return
        else:
            cmseek.warning("No Vulnerabilities discovered in this version of WordPress as of yet")
            return


    return
