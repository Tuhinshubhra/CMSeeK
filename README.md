<p align='center'>
  <img src="https://i.imgur.com/NG51F9o.png" alt="Logo"> <br>
  <img src="https://img.shields.io/badge/Version-1.0%20Beta-brightgreen.svg?style=style=flat-square" alt="version">
  <img src="https://img.shields.io/badge/python-3-orange.svg?style=style=flat-square" alt="Python Version">
  <img src="https://img.shields.io/packagist/l/doctrine/orm.svg?style=style=flat-square" alt="License">
</p>

## What is a CMS?
> A content management system (CMS) manages the creation and modification of digital content. It typically supports multiple users in a collaborative environment. Some noteable examples are: *WordPress, Joomla, Drupal etc*.

## Functions Of CMSeek:
- Basic CMS Detection of over 20 CMS
- Advanced Wordpress Scans
  - Detects Version
  - Detects Users (3 Detection Methods)
  - Looks for Version Vulnerabilities and much more!
- Modular bruteforce system
  - Use pre made bruteforce module or create your own and integrate with it
 
## Requirements and Compatibility:
CMSeeK is built using **python3**, you will need python3 to run this tool and the tool is compitable with **unix based systems** as of now windows support will be added later.

## Installation and Usage:
It is fairly easy to use CMSeeK, just make sure you have python3 and git (just for cloning the repo) installed and use the following command:

- git clone `https://github.com/Tuhinshubhra/CMSeeK`
- cd CMSeeK
- python3 cmseek.py

and the rest should be pretty self explanotory

## Detection Methods:
CMSeek uses mainly 2 things for detection:
- HTTP Headers
- Page Source Code

## Supported CMSs:
CMSeeK currently can detect **22** CMSs you can find the list on [cmss.py](https://github.com/Tuhinshubhra/CMSeeK/blob/master/cmseekdb/cmss.py) file which is present in the `cmseekdb` directory.
All the cmss are stored in the following way:
```
 cmsID = {
   'name':'Name Of CMS',
   'url':'Official URL of the CMS',
   'vd':'Version Detection (0 for no, 1 for yes)',
   'deeps':'Deep Scan (0 for no 1 for yes)'
 }
```

## Scan Result:
All of your scan results are stored in a json file, you can find the logs inside the `Result` directory, and as of the bruteforce results they're stored in a txt file under the site's result directory as well.

Here is an example of the json report log:

![Json Log](https://i.imgur.com/5dA9jQg.png)

## Bruteforce Modules:
CMSeek has a modular bruteforce system meaning you can add your custom made bruteforce modules to work with cmseek. A proper documentation for creating modules will be created shortly but in case you already figured out how to (pretty easy once you analyze the pre-made modules) all you need to do is this:

1. Add a comment exactly like this `# <Name Of The CMS> Bruteforce module`. This will help CMSeeK to know the name of the CMS using regex

2. Add another comment `### cmseekbruteforcemodule`, this will help CMSeeK to know it is a module

3. Copy and paste the module in the `brutecms` directory under CMSeeK's directory

4. Open CMSeeK and Rebuild Cache using `U` as the input in the first menu input.

5. If everything is done right you'll see something like this (refer to below screenshot) and your module listed in bruteforce menu the next time you open CMSeeK.

<p align='center'>
  <img alt="Cache Rebuild Screenshot" width="400px" src="https://i.imgur.com/2Brl7pl.png" />
</p>

## Need More Reasons To Use CMSeeK?
If not anything you can always enjoy exiting CMSeeK *(please don't)*, it will wish you goodbye in a random goodbye message in various languages. 

Also you can try reading comments in the code those are pretty random and weird!!!

## Screenshots:

<p align="center">
  <img alt="Main Menu" width="600px" src="https://i.imgur.com/Nr0ErPW.png" />
  <br><em>Main Menu</em><br>
  <img alt="Scan Result" width="600px" src="https://i.imgur.com/C8SKQ1D.png" />
  <br><em>Scan Result</em><br>
  <img alt="WordPress Scan Result" width="600px" src="https://i.imgur.com/6xWU7W1.png" />
  <br><em>WordPress Scan Result</em><br>
</p>

## Disclaimer:
Usage of CMSeeK for testing or exploiting websites without prior mutual consistency can be considered as an illegal activity. It is the final user's responsibility to obey all applicable local, state and federal laws. Authors assume no liability and are not responsible for any misuse or damage caused by this program.

## License:
CMSeeK is licensed under [MIT License](https://github.com/Tuhinshubhra/CMSeeK/blob/master/LICENSE)

## Follow Me @r3dhax0r:
[Twitter](https://twitter.com/r3dhax0r)    ||    [Facebook](https://fb.com/r3dhax0r)    ||    [Instagram](https://instagram.com/r3dhax0r)