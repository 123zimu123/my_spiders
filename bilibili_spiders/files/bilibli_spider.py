import queue
import json
import requests
from lxml import etree
import threading
from pymongo import MongoClient
import random
#获得视频的json（bv号），保存到mongodb中
user_agent = [
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
      "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
      "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
      "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
      "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
     "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
     "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
     "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
     "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
     "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
     "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
     "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
     "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
     "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
     "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
     "UCWEB7.0.2.37/28/999",
     "NOKIA5700/ UCWEB7.0.2.37/28/999",
     "Openwave/ UCWEB7.0.2.37/28/999",
     "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
      ]
 

class crawl_qiushi:

    def __init__(self):
        self.init_url = "https://api.bilibili.com/x/web-interface/newlist?rid=24&type=0&pn={}&ps=20"
        self.headers = {"User-Agent":random.choice(user_agent)}
        self.url_queue = queue.Queue(10)
        self.html_ret_queue = queue.Queue(10)
        self.html_content_queue = queue.Queue(10)
        self.client = MongoClient(host = "127.0.0.1",port = 27017)
        self.collection = self.client["my_test"]["bilibili_spder"]

    def get_url_queue(self):
        for i in range(1,50):
            self.url_queue.put(self.init_url.format(i))

    def send_url_request(self):
        while True:
            url = self.url_queue.get()
            html_ret = requests.get(url,headers = self.headers)
            self.html_ret_queue.put(html_ret.content.decode("utf-8"))
            self.url_queue.task_done()

    def process_html_ret(self):
        while True:
            ret_json  = self.html_ret_queue.get()
            #html_content = etree.HTML(html_content)
            ret = json.loads(ret_json)#将json转化为字典
            ret = ret['data']['archives']#每一个视频作为一个字典，ret是一个列表，列表中包含了20个字典
            self.html_content_queue.put(ret)
            self.html_ret_queue.task_done()

    def save_content(self):
        while True:
            content = self.html_content_queue.get()#获得的是每一页的内容
            self.collection.insert_many(content)
            self.html_content_queue.task_done()

    def run(self):
        tpool = list()
        t1 = threading.Thread(target=self.get_url_queue)
        tpool.append(t1)
        t2 = threading.Thread(target=self.send_url_request)
        tpool.append(t2)
        t3 = threading.Thread(target=self.process_html_ret)
        tpool.append(t3)
        t4 = threading.Thread(target=self.save_content)
        tpool.append(t4)

        for t in tpool:
            t.setDaemon(True)# 将子线程设置为守护线程，主线程结束，子线程结束
            t.start()

        for p in [self.url_queue,self.html_ret_queue,self.html_content_queue]:
            p.join()#队列将主进程阻塞住，当队列为空时，就不阻塞了,主进程执行结束，子线程从而结束
if __name__ == '__main__':
    crawl_qiushi().run()

# import queue
# import requests
# from lxml import etree
# import threading
# from pymongo import MongoClient

# class crawl_qiushi:

#     def __init__(self):
#         #######
#         self.init_url = "https://www.bilibili.com/v/douga/mad/?spm_id_from=333.5.b_7375626e6176.2#/all/default/0/{}/"
#         #######
#         self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
#         self.url_queue = queue.Queue(10)
#         self.html_ret_queue = queue.Queue(10)
#         self.html_content_queue = queue.Queue(10)
#         self.inner_url_queue = queue.Queue(10)
#         self.client = MongoClient(host = "127.0.0.1",port = 27017)
#         self.collection = self.client["my_test"]["crawl_bilibili_520"]

#     def get_url_queue(self):
#         for i in range(1,20):
#             self.url_queue.put(self.init_url.format(i))

#     def send_url_request(self):
#         while True:
#             url = self.url_queue.get()
#             html_ret = requests.get(url,headers = self.headers)
#             self.html_ret_queue.put(html_ret.content.decode("utf-8"))
#             self.url_queue.task_done()

#     def parse_inner(self):
#         url = self.inner_url_queue.get()
#         url = "https:"+url
#         html_ret = requests.get(url,headers = self.headers)
#         html_ret = etree.HTML(html_ret)
#         comment_number = html_ret.xpath("//div[@id='comment']/div/div/span[1]/text()")[0]
#         dianzan_number = html_ret.xpath("//div[@id='arc_toolbar_report']/div/span[1]/@title")[0]
#         toubi_number = html_ret.xpath("//div[@id='arc_toolbar_report']/div/span[2]/@title")[0]
#         shoucang_number = html_ret.xpath("//div[@id='arc_toolbar_report']/div/span[3]/@title")[0]
#         self.inner_url_queue.task_done()
#         return comment_number,dianzan_number,toubi_number,shoucang_number

#     def process_html_ret(self):
#         while True:
#             html_content = self.html_ret_queue.get()
#             html_content = etree.HTML(html_content)
#             li_list = html_content.xpath("//ul[@class='vd-list mod-2']//li")#li对象的列表
#             content_list = list()
#             for li in li_list:#对每个li对象
#                 item = {}
#                 item["title"] = li.xpath("/div/div[contains(@class,'r')]/a/@title") if len(li.xpath("/div/div[contains(@class,'r')]/a/@title"))>0 else None
#                 item["user"] = li.xpath("/div/div[contains(@class,'r')]/div[@class='up-info']/a/text()")[0] if len(li.xpath("/div/div[contains(@class,'r')]/div[@class='up-info']/a/text()"))>0 else None
#                 item["link"]= li.xpath("/div/div[contains(@class,'r')]/a/@href")[0] if len(li.xpath("/div/div[contains(@class,'r')]/a/@href"))>0 else None
#                 self.inner_url_queue.put(item["link"])
#                 item["comment_number"],item["dianzan_number"],item["toubi_number"],item["shoucang_number"] = self.parse_inner()
#                 content_list.append(item)#content_list中放的是一页中所有需要的内容,里面每个元素是字典,字典中存放的是每个li中我们爬取的内容
#             self.html_content_queue.put(content_list)
#             self.html_ret_queue.task_done()

#     def save_content(self):
#         while True:
#             content = self.html_content_queue.get()#content的内容是每一页的内容
#             if(len(content)==0):
#                 pass
#             else:
#                 self.collection.insert_many(content)
#                 self.html_content_queue.task_done()

#     def run(self):
#         tpool = list()
#         t1 = threading.Thread(target=self.get_url_queue)
#         tpool.append(t1)
#         t2 = threading.Thread(target=self.send_url_request)
#         tpool.append(t2)
#         t3 = threading.Thread(target=self.process_html_ret)
#         tpool.append(t3)
#         t4 = threading.Thread(target=self.save_content)
#         tpool.append(t4)

#         for t in tpool:
#             t.setDaemon(True)# 将子线程设置为守护线程，主线程结束，子线程结束
#             t.start()

#         for p in [self.url_queue,self.html_ret_queue,self.html_content_queue]:
#             p.join()#队列将主进程阻塞住，当队列为空时，就不阻塞了,主进程执行结束，子线程从而结束
# if __name__ == '__main__':
#     crawl_qiushi().run()

