#!/usr/bin/python3
'''
使用request爬取github特定code代码SHODAN_API_KEY的数据

author: s1g0day
time: 2021/10/28
version: '0.2'

目前已实现，爬取一页的数据，并提取出 ***SHODAN_API_KEY*** = xxx 的值
待解决的问题
1.访问速率问题
    当访问速率偏高时,会被github限制速率(您已超出二级速率限制)，此时状态码为429,页面长度为9270
    暂时解决方法是通过sleep 来扩大每次访问的间隔时间
2.github返回的数据不同
    当p=100时(99也一样其他页码没有测试)，发现获取到的数据不同
3.脚本跑的有些慢
'''

import re
import requests
import html
import time
import os.path
import shodan
import csv
from bs4 import BeautifulSoup

def get_req(url, reqsession, page):

    proxies = {
        'http':'socks5h://127.0.0.1:1080',
        'https':'socks5h://127.0.0.1:1080'
    }
    
    # 只能用cookie
    headers={
        'cookie': '_octo=GH1.1.1826189760.1631975164; _device_id=9c7223facc4c34c4251bfcdcccea7205; user_session=NxAkpxuMoGegoHXIn3SMdk_sgKUph4hPm58QolsjZe3qDMTi; __Host-user_session_same_site=NxAkpxuMoGegoHXIn3SMdk_sgKUph4hPm58QolsjZe3qDMTi; logged_in=yes; dotcom_user=s1g0day; has_recent_activity=1; color_mode={"color_mode":"light","light_theme":{"name":"light","color_mode":"light"},"dark_theme":{"name":"dark","color_mode":"dark"}}; tz=Asia/Shanghai; _gh_sess=OqonKCRdAkPwU/6X9HzBfdGFf34/uAZkgF8nskpR+yDdSqwtg6UmkLJokBPXGSv63MP3nzGYsHAdd9iM3Rk7r2JJ65hJ66c7wIgS+cAJBUqNQ2LijDK1u/jPfa6ypiaKwKzHFQRCWAPbpg4Q4FbnW3kYg50L8WvLGmqETArGfehGWiAgJFNJZk1lpde/qUoCdzIPfNXI9afA/6NAJ5jfCt8Fy6mf6u2/y3q531DeA4O3iTZrXL97GbdTsvgag6WQg6xMHvqNRitd8Ou3P1PlHjqwXkDl5a9OCypGN24zZ3a26ieoD+2oiL3h8C1R1dT6G/4AWkoKrlZyOBlPSQeR7ONRHra2YuFj0/0DmLBXHrER587iAWWS3dYKWMopIWriMvJ2PDre4CS83GrbRDQacc9GnDXPX/Aa8vkzKB2Nmrj79k/XPC7EDkHpF2l1v2dGWlqm/5QD+iOeHu2qTLW8xD0n0G2Wy3yfpoOc0ZZK5Vr9gtoGnqleAtIhJvdt+XNCGhopNRKxmTovBva2F+gNoCeBem53IWYgB8osfg==--AbxQFVmlIbAWlp/z--W5SdQ657muN3/s3LpTTlhw=='
    }
    
    try:
        req = reqsession.get(url=url, proxies=proxies,headers=headers)
        req.encoding = req.apparent_encoding
        status_code = req.status_code
        log = "\n[+]Try url: '" + url + "'\tstatus_code: " + str(status_code) + "\tpage: " + str(page)
        if status_code == 404:
            print("status_code: ",status_code)
            exit()
        elif status_code == 429:
            print("被github限制速率了，暂停11秒")
            time.sleep(11)
        else:
            print(log)
            return req
    except:
        print("连接错误")
        exit()

def get_list(url, reqsession, page):

    datas = get_req(url, reqsession, page)
    text = datas.text
    # html实体化字符转原格式
    s = html.unescape(text)
    #去除html标签
    pattern = re.compile(r'<[^>]+>',re.S)
    result = pattern.sub('', s)
    #以\n为分隔符分出列表
    result = result.split("\n")
    for i in range(len(result)):
        if len(result[i]) > 34:
            shodanlist = result[i]
            shodan_list(shodanlist)
    time.sleep(10)

def shodan_list(shodanlist):
    
    # 因为有些SHODAN_API_KEY是小写,find无法匹配到,因此只在比较的时候转为小写
    if shodanlist.upper().find("SHODAN_API_KEY") > -1 and shodanlist.upper().find("=") > -1:
        # print(shodanlist)
        keydatas = shodanlist.split("=")[1]
        if 34<= len(keydatas) <=36 and keydatas.count("xxxx") == 0:
            if "'" in keydatas or '"' in keydatas:
                keydatas = eval(keydatas)
                if keydatas and keydatas not in shodankeylist:
                    print(keydatas)
                    shodankeylist.append(keydatas)
                    key = shodanscan_credits(keydatas)
                    save_info(key, fname)
                    

def shodanscan_credits(keydatas):
    # 用于检测shodan的API KEY积分,65536为高级会员,100为普通用户
    api = shodan.Shodan(keydatas.strip())

    try:
    # Search Shodan
        results = api.info()
        pylog = key.strip() + "," + str(results["scan_credits"]) + "," + str(results["query_credits"]) + "," + str(results["monitored_ips"])
        csvfile.writerow(pylog.split(",")) 
        return key.strip()
    except shodan.APIError as e:
        print('Error: {}'.format(e))
        return "Error"
    time.sleep(1)
    
def save_info(key, fname):
    # 用于检查字符串在不在文件内,如果不在就添加到文本，如果在就pass
    with open(fname,"r") as fileshodan:
        fileshodan = fileshodan.readlines()
        if key+"\n" in fileshodan:
            print("文件中存在:",key)
        elif key == "Error":
            pass
        else:
            shodankey_txt = open(fname, "a+" , encoding="utf-8")
            shodankey_txt.write(key + "\n")
            shodankey_txt.close

def shodan_main(fname):
    
    reqsession = requests.Session()
    for i in range(1,4):
        if os.path.isfile(fname) == False:
            open(fname,"a").close
    
        if i == 1:
            urlfile = "https://github.com/search?q=in:file SHODAN_API_KEY&type=Code"
        else:
            urlfile = "https://github.com/search?p=" + str(i) + "&q=in:file SHODAN_API_KEY&type=Code"
            
        get_list(urlfile, reqsession, i)

if __name__ == "__main__":
    shodankeylist = []
    fname = "shodankey.txt"
    csvfile = "shodankey.csv"
    with open(csvfile,'a+',newline='', encoding='utf-8')as resultFile:
        RESULT = ['hangyeid','site','rank']    # 设置表头 三个列名
        csvfile = csv.writer(resultFile,dialect ='excel')    # 定义类型
        csvfile.writerow(RESULT)    # 将表头写入文件
        # save_csv(csvfile)    #获取数据
    shodan_main(fname)
    print(shodankeylist)
    
