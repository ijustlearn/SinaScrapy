# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest,Request
import json
from scrapyPro1.items import Info
import random

class SinascrapySpider(scrapy.Spider):
    name = "sinaScrapy"
    #allowed_domains = ["sina.com"]
    #start_urls = ['https://passport.weibo.cn/signin/login']
    start_id = set([6109436574,5748821494,1807149297,2419336232])
    finish_id = set()
    crawled_info_id = set()
    def start_requests(self):
        for id in self.start_id:
            yield Request('http://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_'+str(id)+'&page=1',callback=self.parse0,meta={'page':1,'id':id})

    def parse0(self,response):
        print('粉丝页面返回的url is : ' + response.url)
        print('本次request的COOKIE是：' + str(response.request.cookies))
        data = json.loads(response.body_as_unicode())
        page = response.meta['page']+1
        id = response.meta['id']
        try:
            for list in data['cards'][0]['card_group']:
                info = Info()
                info['id'] = list['user']['id']

                info['name'] = list['user']['screen_name']
                desc = list['desc2']
                info['fanstotal'] = desc.split('：')[1]
                if info['id'] not in self.finish_id:
                    yield Request(
                        'http://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_' + str(
                            info['id']) + '&page=1',
                        callback=self.parse0, meta={'page': 1, 'id': id})
                if info['id'] not in self.crawled_info_id:
                    yield Request('http://m.weibo.cn/api/container/getIndex?containerid=230283'+str(info['id'])+'_-_INFO',callback=self.parse1,meta={'info':info})

            yield Request('http://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_'+str(id)+'&page='+str(page),meta={'page':page,'id':id},callback=self.parse0)
        except (KeyError,IndexError)   as e :
            print('已经爬完了'+str(id)+'的可爬取粉丝')
        finally:
            self.finish_id.add(id)
    #个人信息爬取
    def parse1(self,response):
        info = response.meta['info']
        data = json.loads(response.body_as_unicode())
        infodict = {}
        try:
            for card in data['cards']:
                for item in card['card_group']:
                    item_name = item.get('item_name',None)
                    item_content = item.get('item_content',None)
                    if item_name and item_content :
                        infodict[item['item_name']]=item['item_content']
            info['sex']=infodict.get('性别','')
            info['city'] = infodict.get('所在地','')
            info['desc'] = infodict.get('简介','')
            info['school'] = infodict.get('学校','')
            info['level'] = infodict.get('等级','')
            info['createDate'] = infodict.get('注册时间','')
            return info
        except (KeyError,IndexError) as e :
            print(str(info['id'])+" 查询不到基本信息")
        finally:
            self.crawled_info_id.add(info['id'])