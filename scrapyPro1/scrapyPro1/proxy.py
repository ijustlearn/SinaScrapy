import requests
import json,random
import requests.exceptions
import threading
from  scrapyPro1.scrapyPro1.user_agents  import agents
url = 'https://www.sina.com'
deleteUrl = 'http://118.89.228.18:8000/delete?ip='
PROXY_IP_LIST = []

def get_Seed_IP():
    proxyUrl = 'http://118.89.228.18:8000/?protocol=0&count=100'
    r = requests.get(proxyUrl)
    ipdict = json.loads(r.content.decode('utf-8'))
    return ipdict
begin_ip_list = get_Seed_IP()
def checkPIP():
    global PROXY_IP_LIST,begin_ip_list
    ProIPList = []
    r1 = None

    while True:
        try:
            if len(begin_ip_list)==0:
                break
            proxyip = begin_ip_list.pop()
            proxy = {
                "http": 'http://%s:%s' % (proxyip[0], proxyip[1]),
                "https": 'http://%s:%s' % (proxyip[0], proxyip[1])
            }
            headers = random.choice(agents)
            #print(proxy)
            r1 = requests.get(url,headers={'User-Agent':headers},proxies=proxy,timeout=5)

            if r1.ok :
                ProIPList.append(proxyip[0])
                ProIPList.append(proxyip[1])
                print('获取到一个可用IP')
                break
        except (requests.exceptions.ProxyError,requests.exceptions.ReadTimeout,requests.exceptions.ConnectTimeout,requests.exceptions.ConnectionError) as e :
            #print(str(proxyip) + ' 不能正常使用,即将删除该IP')
            r2 = requests.get(deleteUrl+proxyip[0])
            if json.loads(r2.content.decode('utf-8'))[1] == 1 :
                print(str(proxyip) + '不能正常使用,删除成功')
    #print('结束查找代理IP，IP池为：'+str(ProIPList))
    PROXY_IP_LIST.append(ProIPList)
def getProxyIP():
    print('开始获取代理IP')
    global PROXY_IP_LIST
    threads = []
    for i in range(10):
        t = threading.Thread(target=checkPIP,daemon=True)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print('结束获取代理IP')
    return PROXY_IP_LIST
if __name__=="__main__":
    print(getProxyIP())
    #删除所有代理IP，避免好多有问题
    # proxyUrl = 'http://118.89.228.18:8000'
    # r = requests.get(proxyUrl)
    # ipdict = json.loads(r.content.decode('utf-8'))
    # while len(ipdict)>0:
    #     deleteUrl = 'http://118.89.228.18:8000/delete?ip='
    #     proxyip = ipdict.pop()
    #     r2 = requests.get(deleteUrl + proxyip[0])
    #     if json.loads(r2.content.decode('utf-8'))[1] == 1:
    #         print(str(proxyip) + ' 删除成功')