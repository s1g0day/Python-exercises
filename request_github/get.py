#!/usr/bin/python3
'''
使用request爬取github特定code代码SHODAN_API_KEY的数据

author: s1g0day
time: 2021/04/15
version: '0.1'

目前已实现，爬取一页的数据，并提取出 ***SHODAN_API_KEY*** = xxx 的值
待解决的问题
1.访问速率问题
    当访问速率偏高时,会被github限制速率(您已超出二级速率限制)，此时状态码为429,页面长度为9270
2.github返回的数据不同
    当p=100时(99也一样其他页码没有测试)，发现获取到的数据不同

'''

import re
import requests
import html
from bs4 import BeautifulSoup

def get_req(url, reqsession):
    
    
    proxies = {
      "http": "http://127.0.0.1:1080",
      "https": "http://127.0.0.1:1080"
    }
    
    # 只能用cookie
    headers={
        'cookie': 'xxx'
    }
    
    try:
        req = reqsession.get(url=url, proxies=proxies,headers=headers)
        req.encoding = req.apparent_encoding
        print(req.status_code)
        return req
    except:
        print()
        exit()

def get_shodanlist(url, reqsession):

    datas = get_req(url, reqsession)
    text = datas.text
    s = html.unescape(text) # html实体化字符转原格式
    
    #去除html标签
    pattern = re.compile(r'<[^>]+>',re.S)
    result = pattern.sub('', s)
    
    result = result.split("\n") #以\n为分隔符分出列表
    shodan_list(result)

def shodan_list(result):
    for i in range(len(result)):
        if len(result[i]) > 34:
            shodanlist = result[i]
            
            # 因为有些SHODAN_API_KEY是小写,find无法匹配到,因此只在比较的时候转为小写
            if shodanlist.upper().find("SHODAN_API_KEY") > -1 and shodanlist.upper().find("=") > -1:
                # print(shodanlist)
                denghaohou = shodanlist.split("=")[1]
                if 34<= len(denghaohou) <=36 and denghaohou.count("xxxx") == 0:
                    # if "'" in denghaohou or '"' in denghaohou:
                    denghaohou = eval(denghaohou)
                    print(denghaohou)

def main():
    reqsession = requests.Session()
    # for i in range(1):
    url = "https://github.com/search?p=99&q=in:file SHODAN_API_KEY&type=Code"
    # url = "https://github.com/search?p=99&q=in:path SHODAN_API_KEY&type=Code"
    get_shodanlist(url, reqsession)

if __name__ == "__main__":
    main()
