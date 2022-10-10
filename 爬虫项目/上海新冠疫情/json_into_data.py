import pymongo
import json
from bson import ObjectId
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# 创建数据库
mydb = myclient["COVID-19"]
# 创建集合,就是类似表
mycol = mydb["上海"]
with open('D:/liu.json', 'r', encoding='UTF-8') as f:
    res = f.read()
    result = json.loads(res)
    for i in result:
        # 把str类型转换成mongodb里的对应类型
        i['_id'] = ObjectId(i['_id'])
        # 如果想要重新自动生成id就在在这里把id字段删了
        # del i['_id']
    mycol.insert_many(result)