import pymongo
import json
import re
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["COVID-19"]
mycol = mydb["上海"]
temp = []
for x in mycol.find():
    # 因为collection.find()得到的字段_id是自动生成的ObjectId
    # 所以需要转换成str格式否者无法存入json
    x['_id'] = re.findall("'(.*)'",x.get('_id').__repr__())[0]
    temp.append(x)
with open('D:/liu.json','w',encoding='UTF-8') as f:
  	f.write(json.dumps(temp,indent=2))