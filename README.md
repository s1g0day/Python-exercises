> 仅仅用来记录写python脚本时的想法及实现代码



判断文件存不存在，若不存在就创建

~~~
import os.path

if os.path.isfile(fname) == False:
    open(fname,"a").close
~~~



检查字符串在不在文件内,如果不在就添加到文本，如果在就pass

    with open(fname,"r") as fileshodan:
        fileshodan = fileshodan.readlines()	#readlines() 用于逐行读取文件
        此时fileshodan是列表,通过if 来判断字符串在不在列表中， 这是绝对匹配
        if keydatas+"\n" in fileshodan:
            print("文件中存在:",keydatas)
        else:
            shodankey_txt = open(fname, "a+" , encoding="utf-8")
            shodankey_txt.write(keydatas + "\n")
            shodankey_txt.close

处理html的返回包

    datas = get_req(url, reqsession, page)
    text = datas.text
    # html实体化字符转原格式
    s = html.unescape(text)
    #去除html标签
    pattern = re.compile(r'<[^>]+>',re.S)
    result = pattern.sub('', s)
    #以\n为分隔符分出列表
    result = result.split("\n")

request经常用的写法

~~~
    proxies = {
    	# 用sock协议时只能用socks5h 不能用socks5,或者用http协议
        'http':'socks5h://127.0.0.1:1080',
        'https':'socks5h://127.0.0.1:1080'
    }
    
    headers={
        'cookie': 'xxx'
        }
    try:
        req = reqsession.get(url=url, proxies=proxies,headers=headers)
        req.encoding = req.apparent_encoding	# apparent_encoding比"utf-8"错误率更低
        status_code = req.status_code
        log = "status_code: " + str(status_code)
        if status_code == 404:
            print("status_code: ",status_code)
            exit()
        else:
            print(log)
            return req
    except:
        print("连接错误")
        exit()
~~~

把`print`的数据保存成`csv格式`的文件

~~~
import csv

def save_csv(csvfile):
    # 保存为csv格式
    hangyeid = "1"
    site = "2"
    rank = 3
    pylog = hangyeid + "," + site + "," + str(rank)
    data = pylog.split(",")    # 将paylog的数据以 逗号(,) 分割成列表  ['1', '2', '3'] 三个列的对应数据
    csvfile.writerow(data)    #写入数据

if __name__=="__main__":
    csvfile = "aizhanph_output.csv"
    with open(csvfile,'a+',newline='', encoding='utf-8-sig')as resultFile:
        RESULT = ['hangyeid','site','rank']    # 设置表头 三个列名
        csvfile = csv.writer(resultFile,dialect ='excel')    # 定义类型
        csvfile.writerow(RESULT)    # 将表头写入文件
        save_csv(csvfile)    #获取数据
~~~

python3 csv写入中文乱码

~~~
# 打开方式应该加上encoding='utf-8-sig'
import csv

data = [['American','美国人'],
        ['Chinese','中国人']]
with open('results.csv','w',newline='',encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerows(data)
~~~


提取去重URL根域名

~~~
import tldextract

domainlist = []
for item in open("target.txt"):
    domain = tldextract.extract(item).registered_domain	#提取根域名
    if domain and not domain in domainlist:	# 检查domain的值为不为空，在不在domainlist列表中，如果不为空且不在列表中，就把domain添加到列表
        domainlist.append(domain)
        print(domain)
~~~

request保持会话session，关闭session

~~~
chongs = requests.Session()
r = chongs.get(url=rnccurl, headers=requests_headers(),timeout=(3.05, 15),verify=False)
r.encoding = 'utf-8'
rncc_text = r.text	# 获取html代码
status_code = r.status_code	#获取状态码
chongs.close()	#关闭session
~~~

request重试

~~~
可以用python官方提供的方法
chongs = requests.Session()
chongs.mount('http://', HTTPAdapter(max_retries=3))
chongs.mount('https://', HTTPAdapter(max_retries=3))

try:
    rnccurl = "https://rank.aizhan.com/"+ domain + "/"
    r = chongs.get(url=rnccurl, headers=requests_headers(),timeout=(3.05, 15),verify=False)
    r.encoding = 'utf-8'
    rncc_text = r.text

except requests.exceptions.ConnectionError as e:
    error = "连接失败，该URL可能被墙掉了"
    print(e+"\n"+error)

chongs.close()	#关闭session

或者用while循环三次
i = 0
while i < 3:
    try:
        r = requests.get(url=url, headers=requests_headers(), timeout=(3.05, 15), verify=False)
        r.encoding = 'utf-8'
        return r.text
    except requests.exceptions.RequestException:
        i += 1	#如果报错 i自增,再次循环重试
        time.sleep(random.randint(10,15))
        return 'error'

~~~

正则获取两个字符之间的数据

~~~
datas = re.findall(r'list":(.+?),"pagestr',domain_text)
~~~

处理返回包的json数据

~~~
r = requests.get(url=domainuel, headers=requests_headers(),timeout=10,verify=False)
r.encoding = 'utf-8'
domaindatas = json.loads(r.text)
print(domaindatas["site"])
~~~

在当前test.py文件中调用hander_random.py内的函数

~~~
#!/usr/bin/python3
# hander_random.py
import random

def random_referer():
	dominio = ['Adzuna', 'Bixee', 'CareerBuilder', 'Craigslist']
	return random.choice(dominio)
def random_useragent():
	locais = ['cs-CZ', 'en-US', 'sk-SK', 'pt-BR', 'sq_AL']
	return random.choice(locais)
~~~

~~~
#!/usr/bin/python3
# test.py
import hander_random

dominio = hander_random.random_referer()
locais = hander_random.random_useragent()
print("dominio: " + dominio + "\tlocais: " + locais)
~~~



python3 调用shodan，检测shodan_api_key的存活

~~~
import time
import shodan

for key in open("shodankey.txt"):
    api = shodan.Shodan(key.strip())
    
    # Wrap the request in a try/ except block to catch errors
    try:
    # Search Shodan
        results = api.info()
        print(key.strip() + "," + str(results["scan_credits"]) + "," + str(results["query_credits"]) + "," + str(results["monitored_ips"]))
    except shodan.APIError as e:
        print('Error: {}'.format(e))
    time.sleep(1)
~~~

Python判断字符串是否为字母或者数字
~~~
严格解析：有除了数字或者字母外的符号（空格，分号,etc.）都会False
isalnum()必须是数字和字母的混合
isalpha()不区分大小写

str_1 = "123"
str_2 = "Abc"
str_3 = "123Abc"

#用isdigit函数判断是否数字
print(str_1.isdigit())
Ture
print(str_2.isdigit())
False
print(str_3.isdigit())
False

#用isalpha判断是否字母
print(str_1.isalpha())    
False
print(str_2.isalpha())
Ture    
print(str_3.isalpha())    
False

#isalnum判断是否数字和字母的组合
print(str_1.isalnum())    
Ture
print(str_2.isalnum())
Ture
print(str_3.isalnum())    
Ture
#注意：如果字符串中含有除了字母或者数字之外的字符，比如空格，也会返回False

if str_3.isalpha():
	print("True")
else:
	print("False")
~~~
正则匹配IP地址
~~~
import re

filelist = ["https://baidu.com","https://192.168.1.1","https://192.168.1.1:8080","192.168.1.1","192.168.1.1:888"]
# 正则匹配IP地址
res = "((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)"
for i in range(len(filelist)):
    if re.search(res, filelist[i]):
        print(filelist[i])
    else:
        pass
~~~
