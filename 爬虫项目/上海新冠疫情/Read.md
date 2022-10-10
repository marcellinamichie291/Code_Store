# 每日疫情人数统计

## insert_data

从百度的每日疫情获取各区新增等数据，然后存入mongodb

[实时更新：新型冠状病毒肺炎疫情地图 (baidu.com)](https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_1&city=上海-上海)

## read_data

从上面数据库中读取数据并展示，其中get_pie传入某个字段以及某一天日期

绘出各区该字段的饼图。get_line传入某个字段以及一段日期序列绘制历史走势图，具体要展示的区在方法里手动改

## export_data

从mongodb数据库导出json文件，用来做数据转移用的

## json_into_data

这个是从json文件导入mongodb使用

# 每日疫情区域分布

## get_lng_lat

从微信发的网页爬取区域分布情况，然后用到百度地图api转换得到经纬度信息

存入local.json文件中。

1、注意代码中的key要进入百度地图api然后点开控制台，选应用管理-我的应用，然后添加一个应用

2、如果json文件中存在{'status': 1, 'msg': 'Internal Service Error:服务器内部错误', 'results': [], 'address': '英伦风尚，'}

这可能是网络交互中出问题了，可以打开文件搜索下

经纬度获取帮助参考：[逆地理编码 gc | 百度地图API SDK (baidu.com)](https://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding)

## get_code

从上面json文件中加载经纬度数据，注意要添加自己的百度key，然后把需要的js代码写到js_code这个txt里面去，最后只要把js_code里面的文字内容复制到一个html中即可。复制位置如下在最后的</script>前面

JS参考代码网页：[地图JS API示例 | 百度地图开放平台 (baidu.com)](https://lbsyun.baidu.com/jsdemo.htm#eMarkerAddEvent)

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <title>点标记添加点击事件</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta http-equiv="X-UA-Compatible" content="IE=Edge">
    <style>
    body,
    html,
    #container {
        overflow: hidden;
        width: 100%;
        height: 100%;
        margin: 0;
        font-family: "微软雅黑";
    }
    </style>
    <script src="//api.map.baidu.com/api?type=webgl&v=1.0&ak=您的kdy"></script>
</head>
<body>
    <div id="container"></div>
</body>
</html>
<script>
var map = new BMapGL.Map('container');

// 创建信息窗口
var opts = {
    width: 200,
    height: 100,
    title: '小区'
};
map.enableScrollWheelZoom(true);
// 初始地址
var point = new BMapGL.Point(121.31184058879414,31.15353065988098);
// 初始聚焦地址，后面数字是初始显示地图大小
map.centerAndZoom(point,18);
    
    
</script>
```

下面程序是指定某个地址获得一个经纬度，可以把这个地址放到上面html中的初始化地址

// 初始地址
var point = new BMapGL.Point(121.31184058879414,31.15353065988098);

```python
import requests
import json
key = '1111'
temp = []
baidu_url = 'https://api.map.baidu.com/geocoding/v3/?address=英伦风尚&city=上海市&output=json&ak='+key
a = requests.get(baidu_url)
print(a.text)
print(json.loads(a.text)['result']['location']['lng'],
      json.loads(a.text)['result']['location']['lat'])
```

