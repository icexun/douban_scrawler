#!/usr/bin/python
# -*- coding: utf8 -*-
__author__ = 'icexun'

import requests
from lxml import html
import re
import Queue
from time import sleep
import cookielib as cookiejar

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

initial_people = 'icesun'
id_queue = Queue.Queue()
# todo_list = []
seen = set()
seen.add(initial_people)
id_queue.put(initial_people)
count = 0

class BlockAll(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

def parse_contacts(people):
    current_list = []
    sleep(6.5)
    print 'parsing user %s' % (people,)
    #hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    #   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    #   'Accept-Encoding': 'none',
    #   'Accept-Language': 'en-US,en;q=0.8',
    #   'Connection': 'keep-alive'
    #}
    #s = requests.session()
    #s.cookies.set_policy(BlockAll())
    #page = s.get("http://api.douban.com/people/" + people + "/contacts?start-index=1&max-results=100000", headers = hdr)
    page = requests.get("http://api.douban.com/people/" + people + "/contacts?start-index=1&max-results=100000?apikey=03ec35f4f29f82bb0bc4a1ded7de8831", timeout=12)
    #xml = html.fromstring(page.content)
    print page.status_code
    tree = html.fromstring(page.content)
    #tree = ET.ElementTree(xml)
    #root = tree.getroot()
    #for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
    for id_url in tree.xpath('//entry/id/text()'):
        # 获取所有关注人的id：格式为http://api.douban.com/people/49312430
        #id_url = entry.find('{http://www.w3.org/2005/Atom}id').text
        ids = re.search(r"\d+", id_url).group(0)
        current_list.append(ids)
    return current_list

# 过滤掉已经在seen_list中的id
# def filt(clist):
#    for i in clist:
#        if (i in seen_list) is False:
#            todo_list.append(i)

def movie_url(id):
    return "movie.douban.com/people/" + id + "/collect" + "\n"

def store_id(id):
    f1 = open(r'C:\Users\Administrator\PycharmProjects\douban\douban_id.txt','a+')
    f1.write(id + '\n')
    f1.close()
    f2 = open(r'C:\Users\Administrator\PycharmProjects\douban\id_moive.txt','a+')
    f2.write(movie_url(id))
    f2.close()

if __name__ == '__main__':
    while True:
        if id_queue.qsize() > 0:
            current_id = id_queue.get()
            id_list = parse_contacts(current_id)
            for ids in id_list:
                if ids not in seen:
                    store_id(ids)
                    id_queue.put(ids)
                    seen.add(ids)
                    count += 1
                    print 'saved %d users' % (count,)
                #sleep(2)
        else:
            break
    print '豆瓣用户id下载完毕！'
