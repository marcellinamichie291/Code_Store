import pymongo
import datetime
import os
# 创建链接
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# 创建数据库
mydb = myclient["COVID-19"]
# 遍历所有集合
collist = mydb.list_collection_names()
# 创建集合,就是类似表
mycol = mydb["上海"]
key_dict = {'累计确诊':'confirmed',
            '累计死亡':'died',
            '累计治愈':'crued',
            '新增确诊':'confirmedRelative',
            '新增本土':'nativeRelative',
            '新增无症状':'asymptomaticRelative'}


# 全部数据显示
def total_data(date_):
    # 读取当天数据信息
    myquery = {"date": date_}
    mydoc = mycol.find_one(myquery)
    print('上海市')
    for i in key_dict:
        print(i, mydoc[key_dict[i]])
    for i in mydoc['subList']:
        print(i['city'])
        for j in key_dict:
            print(j, i[key_dict[j]])
        print('--------------------------------------------------------')


# 返回某个区的某个字段
def district_pie(covid_key, date_):
    # 读取当天数据信息
    myquery = {"date": date_}
    mydoc = mycol.find_one(myquery)
    x = []
    y = []
    for i in mydoc['subList']:
        x.append(i['city'])
        try:
            y.append(i[covid_key])
        except:
            y.append(0)
    return x, y


# 获取某一天各区分布情况，绘制饼图
def get_pie(covid_key, date_):
    from pyecharts import options as opts
    from pyecharts.charts import Pie
    x, y = district_pie(covid_key, date_)
    c = (
        Pie()
        .add("", [list(z) for z in zip(x, y)])
        .set_global_opts(title_opts=opts.TitleOpts(title=list(key_dict.keys())[list(key_dict.values()).index(covid_key)],
                                                   subtitle=date_),
                         legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .render(r'.\lyy\\'+date_+'_'+covid_key+"_pie.html")
    )
    os.system(r'.\lyy\\'+date_+'_'+covid_key+"_pie.html")


# 获取历史趋势线图
def get_line(covid_key, date_list):
    import pyecharts.options as opts
    from pyecharts.charts import Line
    y_list = []
    x_list = []
    for i in date_list:
        x, y = district_pie(covid_key, i)
        y_list.append(y)
        x_list.append(x)
    x_data = date_list
    city1 = '浦东新区'
    city2 = '松江区'
    city3 = '静安区'
    city4 = '闵行区'
    y_data_1 = [y_list[i][x_list[i].index(city1)] for i in range(len(x_data))]
    y_data_2 = [y_list[i][x_list[i].index(city2)] for i in range(len(x_data))]
    y_data_3 = [y_list[i][x_list[i].index(city3)] for i in range(len(x_data))]
    y_data_4 = [y_list[i][x_list[i].index(city4)] for i in range(len(x_data))]
    y_data_total = []
    for i in range(len(x_data)):
        a = y_list[i]
        b = [int(j) for j in a]
        y_data_total.append(sum(b))
    (
        Line(init_opts=opts.InitOpts(width="1600px", height="800px"))
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="上海市",
            y_axis=y_data_total,
            linestyle_opts=opts.LineStyleOpts(width=2),
        )
            .add_yaxis(
            series_name=city2, y_axis=y_data_2, linestyle_opts=opts.LineStyleOpts(width=2)
        )
            .add_yaxis(
            series_name=city1, y_axis=y_data_1, linestyle_opts=opts.LineStyleOpts(width=2)
        )
            .add_yaxis(
            series_name=city3, y_axis=y_data_3, linestyle_opts=opts.LineStyleOpts(width=2)
        )
            .add_yaxis(
            series_name=city4, y_axis=y_data_4, linestyle_opts=opts.LineStyleOpts(width=2)
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title=
                                      list(key_dict.keys())[list(key_dict.values()).index(covid_key)],
                                      pos_left="center"),
            tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b} : {c}"),
            legend_opts=opts.LegendOpts(pos_left="left"),
            xaxis_opts=opts.AxisOpts(type_="category", name="x"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name="人数",
                splitline_opts=opts.SplitLineOpts(is_show=True),
                is_scale=True,
            ),
        )
            .render(r'.\lyy\\'+covid_key+"_line.html")
    )
    os.system(r'.\lyy\\'+covid_key+"_line.html")


# 日期计算，delta里面填0表示今天，填1表示昨天
today = datetime.datetime.today()
delta = datetime.timedelta(days=0)
ti = (today-delta).strftime('%Y-%m-%d')
# 取从当天往期数几天日期
mongodb_len = mycol.count_documents({})
ti_list = [(today-datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(mongodb_len)]
ti_list = ti_list[::-1]
if __name__ == '__main__':
    get_pie('asymptomaticRelative', ti)
    get_line('asymptomaticRelative', ti_list)
    get_pie('confirmedRelative', ti)
    get_line('confirmedRelative', ti_list)
    myclient.close()
