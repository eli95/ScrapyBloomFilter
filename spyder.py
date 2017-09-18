#! python2
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import re

def spyder_9939(from_page,to_page):
    disease_symptom = pd.DataFrame(columns=['title', 'type', 'html', 'introduction', 'typical_symptom'])
    flag = from_page-1
    for pagenum in range(from_page,to_page):
        page=urllib2.urlopen('http://jb.9939.com/jbzz/?page=%s' %pagenum).read()
        soup = BeautifulSoup(page)
        finder = soup.find_all('div',class_='cation fl')

        if len(finder) != 0:
            for i in finder:
                a = {}
                a['title'] = i.a.get('title')
                a['type'] = i.span.get_text()
                a['html'] = i.a.get('href')
                b = str(a['html'])
                page_introduction = urllib2.urlopen('%sjianjie/' %b).read()
                soup_introduction = BeautifulSoup(page_introduction)

                if a['type'].encode('UTF-8') == '疾病':
                    finder_introduction = soup_introduction.find('div', class_='tost bshare spread graco')
                    a['introduction'] = finder_introduction.p.get_text()

                    page_typical_symptom = urllib2.urlopen('%szz/' % b).read()
                    soup_typical_symptom = BeautifulSoup(page_typical_symptom)
                    finder_typical_symptom = soup_typical_symptom.find('div', class_='tost nickn bshare spread graco')
                    mm = finder_typical_symptom.p.get_text()
                    mm = re.split(r'\s+', mm)
                    nn = ''
                    for i in  mm[1:-1]:
                        nn += i
                        nn += ','
                    a['typical_symptom'] = nn

                else:
                    finder_introduction = soup_introduction.find('div', class_='tost nickn bshare prevp curere spread graco')
                    a['introduction'] = finder_introduction.p.get_text()

                disease_symptom = disease_symptom.append(a,ignore_index=True)
            flag += 1
            print '已爬取第%s页！！！' %flag
        else:
            print '%s页无内容' %pagenum
    disease_symptom.to_csv('data/disease_symptom_%s_%s.csv' %(from_page,to_page),index=False,header=True,encoding='GB18030')
    return '%s页到%s页爬取完毕！！！' %(from_page,to_page-1)