#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
grcl
Copyright (C) 2011  Matt Behrens <askedrelic@gmail.com> http://asktherelic.com

Licensing included in LICENSE.txt
"""

__author__  = "Matt Behrens <askedrelic@gmail.com>"
__version__ = "0.1"

import sys
import logging

import argparse
import libgreader
import util

logging.basicConfig()
logger = logging.getLogger("grcl")

username = 'relic@asktherelic.com'
password = 'testtest'

class GRCL(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self._setupGoogleReader()

    def _setupGoogleReader(self):
        ca = libgreader.ClientAuth(self.username,self.password)
        self.reader = libgreader.GoogleReader(ca)
        self.container = libgreader.SpecialFeed(self.reader, self.reader.READING_LIST)
        self.container.loadItems()

    def _displayFeeds(self, forceRefresh=False):
        if forceRefresh:
            self.container.clearItems()
            self.container.loadItems()

        index = 1
        for item in self.container.getItems():
            title = util.unescape(item.title).replace("\n", ' ').encode('utf-8')
            if len(title) > 80:
                title = title[0:77] + '...'
            author = item.author or ''
            author = author.encode('utf-8')

            if item.isUnread():
                print "%2s: %s [%s]" % (index, title, author)
            index += 1

    def _displayEntry(self, index):
        entry = self.container.items[index-1]
        urls =  util.find_urls(entry.content)
        title = util.unescape(entry.title).replace("\n", ' ').encode('utf-8')
        content = util.strip_tags(util.unescape(entry.content)).encode('utf-8')

        print title
        print content

        #uniqify the urls
        for i in list(set(urls)):
            print ''.join(i)

        #mark entry as read
        #entry.markRead()

    def run(self):
        self._displayFeeds()
        while True:
            opt = raw_input('> ')
            opt = opt.strip().lower()
            if len(opt) == 0:
                self._displayFeeds(True)
            elif opt.find('list') != -1:
                self._displayFeeds()
            else:
                self._displayEntry(int(opt))

if __name__ == '__main__':
    grcl = GRCL(username,password)
    grcl.run()
