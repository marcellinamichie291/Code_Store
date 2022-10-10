from bs4 import BeautifulSoup
import requests
import json
import datetime
import pymongo
# 添加一个时间字段
today = datetime.datetime.today().strftime('%Y-%m-%d')
def get_html():
    url = 'https://voice.baidu.com/act/newpneumonia/' \
          'newpneumonia/?from=osari_pc_1&city=%E4%B8%8A%E6%B5%B7-%E4%B8%8A%E6%B5%B7#tab0'
    r = requests.get(url)
    html = r.text
    # 解析
    soup = BeautifulSoup(html, "html.parser")
    x = json.loads(soup.find('script', {"id":"captain-config"}).get_text()).get('component')[0]
    temp = {}
    # 循环所有城市
    for i in x['caseList']:
        if '上海' in i['area']:
            temp = i
    result = {'date': today}
    result.update(temp)
    return result


# 创建链接
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# 创建数据库
mydb = myclient["COVID-19"]
# 遍历所有集合
collist = mydb.list_collection_names()
# 创建集合,就是类似表
mycol = mydb["上海"]

# 插入数据
def insert_data():
    # 查询指定条件
    myquery = {"date": today}
    mydoc = mycol.find_one(myquery)
    if mydoc == None:
        mycol.insert_one(get_html())
    else:
        myquery = {"date": today}
        newvalues = {"$set": get_html()}
        mycol.update_one(myquery, newvalues)
# 删除数据
def del_data():
    myquery = {"date": today}
    mycol.delete_one(myquery)
    # 删除后输出
    for x in mycol.find():
        print(x)

insert_data()
