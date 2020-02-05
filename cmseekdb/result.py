#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2020 Tuhinshubhra

import cmseekdb.basic as cmseek

def target(target):
    ## initiate the result
    target = target.replace('https://','').replace('http://', '').split('/')
    target = target[0]
    print(' ┏━Target: ' + cmseek.bold + cmseek.red + target + cmseek.cln)

def end(requests, time, log_file):
    ## end the result
    print(' ┃\n ┠── Result: ' + cmseek.bold + cmseek.fgreen + log_file + cmseek.cln)
    print(' ┃\n ┗━Scan Completed in ' + cmseek.bold +cmseek.lblue + time + cmseek.cln +' Seconds, using ' + cmseek.bold + cmseek.lblue + requests + cmseek.cln +' Requests')

def cms(cms,version,url):
    ## CMS section
    print(' ┃\n ┠── CMS: ' + cmseek.bold + cmseek.fgreen + cms + cmseek.cln +'\n ┃    │')
    if version != '0' and version != None:
        print(' ┃    ├── Version: '+ cmseek.bold + cmseek.fgreen + version + cmseek.cln)
    print(' ┃    ╰── URL: ' + cmseek.fgreen + url + cmseek.cln)

def menu(content):
    # Use it as a header to start off any new list of item
    print(' ┃\n ┠──' + content)

def init_item(content):
    # The first item of the menu
    print(' ┃    │\n ┃    ├── ' + content)

def item(content):
    # a normal item just not the first or the last one
    print(' ┃    ├── ' + content)

def empty_item():
    print(' ┃    │')

def end_item(content):
    # The ending item
    print(' ┃    ╰── ' + content)

def init_sub(content, slave=True):
    # initiating a list of menu under a item
    print(' ┃    │    │\n ┃    │    ├── ' + content if slave else ' ┃         │\n ┃         ├── ' + content)

def sub_item(content, slave=True):
    # a sub item
    print(' ┃    │    ├── ' + content if slave else ' ┃         ├── ' + content)

def end_sub(content, slave=True):
    # ending a sub item
    print(' ┃    │    ╰── ' + content if slave else ' ┃         ╰── ' + content)

def empty_sub(slave=True):
    print(' ┃    │    │' if slave else ' ┃         │')


def init_subsub(content, slave2=True, slave1=True):
    # Sub item of a sub item.. this is getting too much at this point
    part1 = ' ┃    │    ' if slave2 else ' ┃         '
    part2 = '│   │' if slave1 else '    │'
    part3 = '\n ┃    │    ' if slave2 else '\n ┃         '
    part4 = '│   ├── ' if slave1 else '    ├── '
    content = part1 + part2 + part3 + part4 + content
    print(content)

def subsub(content, slave2=True, slave1=True):
    part1 = ' ┃    │    ' if slave2 else ' ┃         '
    part2 = '│   ├── ' if slave1 else '    ├── '
    content = part1 + part2 + content
    print(content)

def end_subsub(content, slave2=True, slave1=True):
    part1 = ' ┃    │    ' if slave2 else ' ┃         '
    part2 = '│   ╰── ' if slave1 else '    ╰── '
    content = part1 + part2 + content
    print(content)
