#!/usr/bin/python3
'''
以离线的方式查询大量IP的出现次数及归属地，使用的是https://github.com/lionsoul2014/ip2region的项目
结果保存为CSV格式
'''

import csv
from ip2Region import Ip2Region #此处导入的是刚才复制的py文件

def ip_search():
    #打开需要查询的文件
    with open(search_file,'r',encoding='utf-8') as search_file_r:
        search_file_lines = search_file_r.readlines()
        # print(search_file_lines)
    #准备写入

    searcher = Ip2Region(db_file) #实例化
    for line in search_file_lines:
        if line and line not in iplist:
            jishu = search_file_lines.count(line)
            # print(jishu)
            iplist.append(line)
            ip = line.strip('\n')
            #判断是不是ip，isip这个函数是Ip2Region里写好的，直接用
            if searcher.isip(ip):
                #三种算法任选其一
                data = searcher.btreeSearch(ip) #B树
                # data = searcher.binarySearch(line) #二进制
                # data = searcher.memorySearch(line) #内存
                data = data["region"].decode('utf-8').split("|")
                datas = str(ip) + "," + data[0] + "," + data[2] + "," + data[3] + "," + data[4] + "," + str(jishu) 
                print(datas)
                csvdata = datas.split(",")
                result_file.writerow(csvdata)
            else:
                result_file.writerow('%s|错误数据\n'%ip)
                print('%s|错误数据'%ip)
    searcher.close() #关闭

if __name__ == "__main__":
    iplist = []
    db_file = './ip2region.db'  #数据库文件路径
    search_file = './search_file.txt' #查询文件：每行一个ip
    result_file = './result_file.csv' #结果文件：每行一个ip结果
    with open(result_file,'a+',newline='', encoding='utf-8-sig')as resultFile:
        RESULT = ['IP', "国家", "省份", "城市", "ISP", '出现次数']    # 设置表头 三个列名
        result_file = csv.writer(resultFile,dialect ='excel')    # 定义类型
        result_file.writerow(RESULT)    # 将表头写入文件
        ip_search()
