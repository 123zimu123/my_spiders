import requests
import time
from lxml import etree
import json
import random

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
 
headers = {'User-Agent': random.choice(user_agent)}
url = "http://dsfc.njupt.edu.cn/dsgl/nocontrol/college/dsfcxq.htm"
daoshixingxi_list = list()
with open("daoshibianhao.txt","r",encoding="utf-8") as f:
    while True:
        line = f.readline()
        if not line:
            break
        line = line.split(': "')[1].split('",')[0]
        daoshixingxi_list.append(line)


#content_list = list()


for num in daoshixingxi_list:
    post_data={'zgh': num}
    html_ret = requests.post(url,headers = headers,data=post_data).content.decode("utf-8")
    html_etree = etree.HTML(html_ret)
    item=dict()
    item['姓名'] = html_etree.xpath("//div[@class='control-group']//tr[1]/td[2]/span/text()")[0] if(len(html_etree.xpath("//div[@class='control-group']//tr[1]/td[2]/span/text()")))>0 else None
    item['性别'] = html_etree.xpath("//div[@class='control-group']//tr[1]/td[4]/span/text()")[0] if(len(html_etree.xpath("//div[@class='control-group']//tr[1]/td[4]/span/text()")))>0 else None
    item['导师类型'] = html_etree.xpath("//div[@class='control-group']//tr[1]/td[6]/span/text()")[0] if(len(html_etree.xpath("//div[@class='control-group']//tr[1]/td[6]/span/text()")))>0 else None
    item['技术职称'] = html_etree.xpath("//div[@class='control-group']//tr[2]/td[2]/span/text()")[0] if(len(html_etree.xpath("//div[@class='control-group']//tr[2]/td[2]/span/text()")))>0 else None
    item['邮箱'] = html_etree.xpath("//div[@class='control-group']//tr[2]/td[4]/span/text()")[0] if(len(html_etree.xpath("//div[@class='control-group']//tr[2]/td[4]/span/text()")))>0 else None
    item['学术型硕士招生学科'] = html_etree.xpath("//div[@class='control-group']//tr[3]/td[2]/span/text()")[0] if(len(html_etree.xpath("//div[@class='control-group']//tr[3]/td[2]/span/text()")))>0 else None
    if(len(html_etree.xpath("//div[@class='mb20 editor-area'][1]/p/text()"))==0):
        item['个人简介'] = html_etree.xpath("//div[@class='mb20 editor-area'][1]/text()")[0].replace("\n","").replace("\t","")
    else:
        item['个人简介'] = html_etree.xpath("//div[@class='mb20 editor-area'][1]/p/text()")[0].replace("\n","").replace("\t","")

    if len(html_etree.xpath("//div[@class='mb20 editor-area'][2]/p[2]/text()"))!=0:
        item['研究领域'] = html_etree.xpath("//div[@class='mb20 editor-area'][2]/p[2]/text()")[0].replace("\n","").replace("\t","")
    elif len(html_etree.xpath("//div[@class='mb20 editor-area'][2]/text()"))!=0:
        item['研究领域'] = html_etree.xpath("//div[@class='mb20 editor-area'][2]/text()")[0].replace("\n","").replace("\t","")
    elif len(html_etree.xpath("//div[@class='mb20 editor-area'][2]/p[1]/text()"))!=0:
        item['研究领域'] = html_etree.xpath("//div[@class='mb20 editor-area'][2]/p[1]/text()")[0].replace("\n","").replace("\t","")

    print(item)
    with open("daoshixingxi.txt", "a+", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False, indent=4))
        f.write("\n")
    time.sleep(10)



