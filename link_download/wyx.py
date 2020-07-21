import requests
import json
from lxml import etree

class bilibili_crawl:
    def __init__(self):
        self.url = "https://www.torrentkitty.net/search/{}/{}"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

    def parse_url(self,num):
        #在format('linux')中填入想要查找的内容
        html = requests.get(self.url.format('linux',str(num)),headers = self.headers)
        return html.content.decode()

    def get_content_list(self,html_str):
        html = etree.HTML(html_str.encode("utf-8"))
        td_list = html.xpath("//table[@id='archiveResult']//tr/td[4]")
        content_list = list()
        for td in td_list:#对每个td对象
            item = {}
            item["magnet"] = td.xpath("//a[2]/@href")[5] if len(td.xpath("//a[2]/@href"))>0 else None
            content_list.append(item)
        return content_list

    def save_list(self,content_list,num):
#       print(content_list)
        with open("data{}.txt".format(num),"w",encoding="utf-8") as f:
            f.write(json.dumps(content_list,ensure_ascii=False,indent=4))


    def run(self):
        for i in range(1,10):
            html_str = self.parse_url(i)
            d_list = self.get_content_list(html_str)
            self.save_list(d_list,i)


if __name__ == "__main__":
    test = bilibili_crawl()
    test.run()

