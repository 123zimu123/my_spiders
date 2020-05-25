# coding=utf-8
from pymongo import MongoClient
import pandas as pd
from matplotlib import  pyplot as plt

client = MongoClient()
collection = client["my_test"]["scrapy_qsbk"]
data = collection.find()
data_list = []
for i in data:
    temp = {}
    temp["subs"] = i["subs"]
    temp["comment"] = i['comment']
    data_list.append(temp)
# t1 = data[0]
# t1 = pd.Series(t1)
# print(t1)

df = pd.DataFrame(data_list)

plt.figure(figsize=(20,8),dpi=80)


#scatter使用
#plt.scatter(df['subs'],df['comment'])

#plot使用
#print(df.iloc[:,0])  输出第一列值
#col_values变成了list类型
#print(df.shape,df.shape[0],df.shape[1]) shape[0]是行数
# col = df.iloc[:,-1]
# col_values = col.values
# col_list_values = list(col_values)
# plt.plot(range(df.shape[0]),col_list_values)


#bar使用
plt.bar([0,10,20,30,40],[14,22,15,63,11])

plt.show()