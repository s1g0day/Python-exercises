#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 提取URL主域名

import tldextract
import re

list_domain = []

for item in open("1.txt"):
    if item and not item in list_domain:    # 去空值 将未重复的域名添加到 list_domain 中
        domain = tldextract.extract(item).registered_domain
        list_domain.append(domain)
        if len(domain) != 0:
            print(domain)
        else:
            print(item)
