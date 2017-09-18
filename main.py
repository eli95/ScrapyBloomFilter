#! python2
# -*- coding: utf-8 -*-

import pandas as pd
from multiprocessing import Pool
from spyder import spyder_9939

first_page = 1
last_page = 1499
step = 50

def aggregation():
    print 'aggregation start.'
    forget = []
    target_df = pd.DataFrame(columns=['title', 'type', 'html', 'introduction', 'typical_symptom'])
    for i in range(first_page,last_page,step):
        try:
            target_df = target_df.append(pd.read_csv('data/disease_symptom_%s_%s.csv' %(i,i+step), header=0, encoding='GB18030'),ignore_index=True)
        except:
            forget.append([i,i+step])

    target_df.to_csv('data/disease_symptom_sum.csv',index=False, encoding='GB18030')
    page_forget = pd.DataFrame(forget,columns=['from_page','to_page'])
    page_forget.to_csv('data/forget_pages.csv',index=False)

if __name__ == '__main__':
    p = Pool()
    for i in range(first_page,last_page,step):
        p.apply_async(spyder_9939,args=(i,i+step,))
        print ('任务：%s页--%s页加入进程池' %(i,i+step))
    p.close()
    p.join()
    print 'All subprocesses done.'
    aggregation()
    print 'aggregation completed.'