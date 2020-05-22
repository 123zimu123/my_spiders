from pymongo import MongoClient

client = MongoClient()
collection = client["my_test"]["bilibili_spder"]

bv_list = list()
res = list(collection.find())
for i in res:
    bv_list.append(i['bvid'])


init_url = "https://www.bilibili.com/video/{}"
for i in bv_list:
    print(init_url.format(i))