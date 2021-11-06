#!/usr/bin/python3
# 用于提取文本中的IP和域名

import re
import time

timedata = str(int(time.time()))

IP_vaild = open(timedata+"_ip.txt","a+",encoding="utf-8")
domain_vaild = open(timedata+"_domain.txt","a+",encoding="utf-8")

with open("200.txt") as filelist:
    filelist = filelist.readlines()
    # 正则匹配IP地址
    res = "((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)"
    for i in range(len(filelist)):
        if re.search(res, filelist[i]):
            IP_vaild.write(filelist[i])
        else:
            domain_vaild.write(filelist[i])
            

IP_vaild.close()
domain_vaild.close()
