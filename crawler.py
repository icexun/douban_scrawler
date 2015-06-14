#!/usr/bin/python
# -*- coding: utf8 -*-
__author__ = 'icexun'

import requests
from lxml import html
import re
import Queue
from time import sleep
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

def parse_contacts(people):
    print 'parsing user %s' % people
    current_list = []
    sleep(4)
    r = requests.adapters.HTTPAdapter(max_retries=3)
    try:
        page = requests.get("http://api.douban.com/people/" + people + "/contacts?start-index=1&max-results=100000?apikey=03ec35f4f29f82bb0bc4a1ded7de8831",r,timeout=9)
        print page.status_code
    except:
        print 'failed to get contact list'
        return current_list
    tree = html.fromstring(page.content)
    for id_url in tree.xpath('//entry/id/text()'):
        # 获取所有关注人的id：格式为http://api.douban.com/people/49312430
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
    f1 = open(r'D:\python_projects\douban\douban_id.txt','a+')
    f1.write(id + '\n')
    f1.close()
    f2 = open(r'D:\python_projects\douban\id_movie.txt','a+')
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
                    print 'saved %d users' % count
        else:
            break
    print 'douban user id download completed！'
