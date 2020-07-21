import requests
import os
import json
from lxml import etree
import re
import random
import time

s = requests.session()
s.keep_alive = False

class bilibili_crawl:
    def __init__(self):
        self.url = "https://cdn-yong.bejingyongjiu.com/20200420/9950_24170b87/1000k/hls/index.m3u8"
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"}

    def parse_url(self):
        html = s.get(self.url,headers = self.headers)
        return html.content.decode()

    def get_content(self,html_str):
        ree = re.compile("(.*?).ts")
        d_list = ree.findall(html_str)
        new_d_list = list()
        for i in d_list:
            i=i+".ts"
            new_d_list.append(i)
        
        return new_d_list

    #获取每一个ts文件
    def parse_ts_url(self,d_list):
        for i in d_list:
            url = "https://cdn-yong.bejingyongjiu.com/20200420/9950_24170b87/1000k/hls/"+i;
            html = s.get(url,headers = self.headers)
            html = html.content
            with open(i,"wb+") as f:
                f.write(html)
            time.sleep(5)
   
    def merge(self):
        #合并ts文件
        s = r"copy /b *.ts a.mp4"
        os.chdir("E://PyCharm 2019.2.4//project//vedio_crawl//my_test")
        os.system(s)

    def save_list(self,d_list):
        with open("data.txt","a",encoding="utf-8") as f:
            f.write(json.dumps(d_list,ensure_ascii=False,indent=4))


    def run(self):
        # html_str = self.parse_url()
        # d_list = self.get_content(html_str)
        # # print(d_list)
        # self.parse_ts_url(d_list)
        self.merge()

if __name__ == "__main__":
    test = bilibili_crawl()
    test.run()

