#!/usr/bin/python3
# 获取代理池

import requests
import random
import time
from bs4 import BeautifulSoup
def get_proxy():
    '''
    爬取快代理网站，爬取第一页代理，时间可保证在当天时间，后续页代理不可靠
    :return: 代理列表
    '''

    content=requests.get("https://www.kuaidaili.com/free/inha/1/")
    content.encoding=content.apparent_encoding
    text=content.text
    soup=BeautifulSoup(text,'html.parser')
    soup=soup.tbody
    IPS=soup.find_all(attrs={'data-title':'IP'})
    print(IPS)
    PORTS=soup.find_all(attrs={'data-title':'PORT'})
    for i in range(0,len(IPS)):
        proxy='%s:%s' %(IPS[i].string,PORTS[i].string)
        proxys.append(proxy)

def random_proxy():
    '''
    将获取到的proxy进行随机化获取，每次调用该函数，代理不唯一
    :return:   proxy
    '''
    proxy=proxys[random.randint(0,len(proxys)-1)]
    return proxy

def reques():
    proxies = {'http': 'http://%s' % (random_proxy())}
    req = requests.get("https://baidu.com", proxies=proxies)
    return req.status_code

if __name__ == "__main__":
    proxys=[]
    get_proxy()
    time.sleep(2)
    print(random_proxy())
    print(reques())
