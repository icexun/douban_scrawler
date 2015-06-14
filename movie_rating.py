#!/usr/bin/python
# -*- coding: utf8 -*-
__author__ = 'ice'

import requests
import lxml.html.soupparser as soupparser
import lxml.etree as etree
import re
from time import sleep
#import cPickle as p
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

apikey = '?apikey=03ec35f4f29f82bb0bc4a1ded7de8831'
count = 0

def read_url():
    f = open(r'D:\python_projects\douban\id_movie_1.txt','r')
    for url in f:
        url = url.strip()
        store_movie(url)
    print 'Congratulations!!! Movie rating saved for all users!'

def store_movie(url):
    global count
    initial_url = url
    ids = str(re.search(r'\d+', url).group(0))
    d0 = {}
    d = {}
    print 'save rating for user %s'% ids
    u = 'http://' + initial_url + apikey
    while True:
            n, d0 = parse_moive(u,d0)
            if n:
                u = n
            else:
                break
    count += 1
    fn = ( count / 1000 )
    d[ids] = d0
    filename = r'D:\python_projects\douban\rating' + str(fn) + '.txt'
    f = open(filename, 'a+')
    #p.dump(d, f)
    json.dump(d, f, ensure_ascii=False, encoding='utf-8')
    f.write('\n')
    f.close()
    print "all movie rating saved for user %s" % ids
    print 'saved %d users' % count

def parse_moive(url,d0):
    print 'parsing url %s'% url
    next_url = ''

    sleep(10)
    r = requests.adapters.HTTPAdapter(max_retries=3)
    try:
        html = requests.get(url, r, timeout=9)
        print html.status_code
    except:
        print 'failed to get response from url'
        return next_url,d0
    dom = soupparser.fromstring(html.content)
    body = dom[1]

    articlelist = body.xpath("//div[@class='item']")

    for article in articlelist:
        articlestr = etree.tostring(article)
        articlebody = soupparser.fromstring(articlestr)
        t = articlebody.xpath("//a")
        turl = t[0].values()[1]
        title = t[0].values()[2]
        movieid = '['+ title + ']' + turl
        try:
            rate = re.search(r'<span class="rating(\d)-t"/>', articlestr).group(1)
        except AttributeError:
            rate = '0'
        print 'rating is %s' % rate
        d0[movieid] = rate

    nextpage = body.xpath("//link[@rel='next']")
    try:
        next_url = nextpage[0].values()[0]
    except IndexError:
        pass
    return next_url,d0

if __name__ == '__main__':
    read_url()