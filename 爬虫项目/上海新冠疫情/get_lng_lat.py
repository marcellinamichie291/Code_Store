import urllib.request
import re
from bs4 import BeautifulSoup
import json
import requests
import queue
q = queue.Queue()
url_ = 'https://mp.weixin.qq.com/s/uj4TYASUn2YJZQMg2aUvdw'
response = urllib.request.urlopen(url_)
# 提取响应内容
htmlx = response.read().decode('utf-8')
htmly= re.sub(r'<br\s+?/>', '', htmlx)
htmlz= re.sub(r'<span style="font-family: mp-quote, -apple-system-font, BlinkMacSystemFont, Arial, sans-serif;">', "", htmly)
html= re.sub(r'(分别)?居住于[，。：]?</span>', "</span>", htmlz)
bf = BeautifulSoup(html,"html.parser")
div = bf.find_all('div', class_='rich_media_content')
a_bf = BeautifulSoup(str(div[0]), "html.parser")
span = a_bf.find_all("span")
# 获取位置地址
locatlon_list = []
for item in span:
    s=str(item.string)
    if  s.find('相关居住地')==-1 and s.find('资料')==-1 and  s.find('编辑')==-1 and s!='None' and not('新增') in s and not('各区信息如下') in s:
        locatlon_list.append(s)
# 去重
locatlon_list = list(set(locatlon_list))
# 把上面的小区地理名称传入百度地理编码返回经纬度
key = '111'
temp = []
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

input_task = locatlon_list
def my_func(x):
    baidu_url = 'https://api.map.baidu.com/geocoding/v3/?address='+x+'&city=上海市&output=json&ak='+key
    a = requests.get(baidu_url)
    dic_ = json.loads(a.text)
    dic_['address'] = x
    return dic_
def multi_thread():
    with ThreadPoolExecutor() as pool:
        results = pool.map(my_func, input_task)
    for out in results:
        temp.append(out)
multi_thread()
# 把经纬度信息存入json
with open('local.json', 'w', encoding='utf-8') as f:
    json.dump(temp,f,ensure_ascii=False,indent=2)