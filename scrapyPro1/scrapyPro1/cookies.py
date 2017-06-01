import requests
import random
from scrapyPro1.scrapyPro1 import proxy,config
userlist = config.USERLIST
def get_cookie(username,password,proxyip=None):
    if proxyip :
        proxies =  {"http": "http://%s:%s"  % (proxyip[0],proxyip[1]),"https":"http://%s:%s"  % (proxyip[0],proxyip[1]), }
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
               'Referer':'https://passport.weibo.cn/signin/login',
               'Host':'passport.weibo.cn',
               'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
               }
    s = requests.session()
    postdata={
                'username': username,
                'password': password,
                'savestate': '1',
                'ec': '0',
                'entry': 'mweibo',
                'mainpageflag': '1'
            }
    postUrl = 'https://passport.weibo.cn/sso/login'
    response = s.post(postUrl,data=postdata,headers=headers,proxies=proxies)
    cookie = response.cookies.get_dict()
    return cookie
def get_cookies():
    cookies = []
    for k,v in userlist.items():
        cookies.append(get_cookie(k,v))
    return cookies
class   My_Cookies(object):
    def __init__(self):
        self.proxylist = proxy.getProxyIP()
        self.userlist = config.USERLIST
        self.CookieAndProxy = []
    def get_cookie(self):
        for k,v in self.userlist.items():
            proxyip = random.choice(self.proxylist)
            cookie = get_cookie(k,v,proxyip)
            CP = {'proxyip':proxyip,'cookie':cookie}
            self.CookieAndProxy.append(CP)
    def get_cookie_and_proxyip(self):
        return self.CookieAndProxy
if __name__ == '__main__':
    cookies = My_Cookies()
    cookies.get_cookie()
    print(cookies.get_cookie_and_proxyip())