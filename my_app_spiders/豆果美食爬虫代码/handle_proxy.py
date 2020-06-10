import requests

#114.246.2.155"
url = 'http://ip.hahado.cn/ip'
#{'http':'http://用户名:密码@ip代理服务器地址:端口号'}
proxy = {'http':'http://H211EATS9O5745KC:F8FFBC929EB7D5A7@http-cla.abuyun.com:9030'}
response = requests.get(url=url,proxies=proxy)
print(response.text)