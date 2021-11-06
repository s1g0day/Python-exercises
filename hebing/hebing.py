#!/usr/bin/python3

'''
两个文件进行对比取出重复的内容和所有去重后的结果
1.把两个文件分别写入到列表中
2.把重复的部分写入到新的文件中
3.把两个文件合并写入一个新文件用于后期提交报告检索，然后去重再写一个新文件用于后期爆破子域名,
'''
import time
import os
import os.path

#创建字典
def dictlist(filepath):
    dicts = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return dicts


def filecaozuo():
    triks = str(int(time.time()))
    f1=open(triks+"_btvuaz_twoall.txt","a+",encoding='utf-8')
    f2=open(triks+"_btvuaz_hebing.txt","a+",encoding='utf-8')
    f3=open(triks+"_btvuaz_chongfu.txt","a+",encoding='utf-8')

    print("原dicts1: ",len(dicts1))
    print("原dicts2: ",len(dicts2))
    
    for line in dicts2:
        dicts1.append(line)
        
    print("合并dicts1,dicts2: ",len(dicts1))
    
    for line in dicts1:
        f1.write(line.strip()+"\n")
        if line and line not in hebing:
            hebing.append(line)
            f2.write(line.strip()+"\n")
        else:
            chongfu.append(line)
            f3.write(line.strip()+"\n")

    print("合并去重后: ",len(hebing))
    print("重复: ",len(chongfu))

    f1.close()
    f2.close()
    f3.close()

if __name__ == '__main__':
    hebing = []
    chongfu = []

    dicts1 = dictlist('1634905911_btvu_hebing.txt')
    dicts2 = dictlist('1634905451_aizhandomain_nogov.txt')
    filecaozuo()
    print("\n<<<success>>>")
