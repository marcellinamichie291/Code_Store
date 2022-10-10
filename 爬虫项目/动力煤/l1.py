from bs4 import BeautifulSoup
import requests
import pymongo
# 创建链接
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# 创建数据库
mydb = myclient["大众商品"]


# 如果是网页的话这种方式获取,这里做范例用本地文件来读取
code = 'SA'
url_or = r'http://soda.100ppi.com/kx/list---'
num = 5
url_list = [url_or + str(i) + '.html' for i in range(1,num+1)]

mycol = mydb[code]
for url in url_list:
    r = requests.get(url)  
    html = r.text
    # 解析
    soup = BeautifulSoup(html,"html.parser")
    div2 = soup.find_all('div',class_="pr-news-tit")
    for i in div2:
        start = i.text.split()[0].index('为')
        price = i.text.split()[0][start+1:]
        date = i.text.split()[1]
        # 查询数据
        myquery = { "date":date+' 00:00:00'}
        num = mycol.count_documents(myquery)
        if num == 0:
            # 插入数据
            mydict = { "date":date+' 00:00:00', "price":price}
            mycol.insert_one(mydict)
            print(date+' 00:00:00',price)