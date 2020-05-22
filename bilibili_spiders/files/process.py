from pymongo import MongoClient
from lxml import etree
import requests
import random
import threading
import json
import queue
#通过bv号发送请求，提取点赞投币收藏观看数
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
        self.init_url = "https://www.bilibili.com/video/{}"
        self.headers = {"User-Agent":random.choice(user_agent)}
        self.url_queue = queue.Queue(10)
        self.html_ret_queue = queue.Queue(10)
        self.html_content_queue = queue.Queue(10)
        self.client = MongoClient(host = "127.0.0.1",port = 27017)
        self.collection = self.client["my_test"]["bilibili_spder"]
        self.collection_store = self.client["my_test"]["bilibili_video_info"]
    def get_url_queue(self):
        bv_list = list()
        res = list(self.collection.find())#一般来说我们把find()的结果转化为list类型
        for i in res:
            bv_list.append(i['bvid'])
        for i in bv_list:
            self.url_queue.put(self.init_url.format(i))

    def send_url_request(self):
        while True:
            url = self.url_queue.get()
            html_ret = requests.get(url,headers = self.headers)
            self.html_ret_queue.put(html_ret.content.decode("utf-8"))
            self.url_queue.task_done()

    def process_html_ret(self):
        while True:
            ret = self.html_ret_queue.get()
            html_content = etree.HTML(ret)
            item=dict()
            item['comment'] = html_content.xpath("//span[@class='b-head-t results']/text()")[0] if len(html_content.xpath("//span[@class='b-head-t results']/text()"))>0 else None
            item['coin'] = html_content.xpath("//span[@class='coin']/@title")[0] if len(html_content.xpath("//span[@class='coin']/@title"))>0 else None
            item['collect'] = html_content.xpath("//span[@class='collect']/@title")[0] if len(html_content.xpath("//span[@class='collect']/@title"))>0 else None
            #item['title'] = html_content.xpath("//span[@class='tit']/text()")[0] if len(html_content.xpath("//span[@class='tit']/text()"))>0 else None

            self.html_content_queue.put(item)#结果是一个字典，包含一个视频的信息
            self.html_ret_queue.task_done()

    def save_content(self):
        while True:
            content = self.html_content_queue.get()#获得的是每个视频的内容
            self.collection_store.insert_one(content)
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



