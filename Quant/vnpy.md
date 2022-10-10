# 常规说明

## 常用类

```python
# ui界面增加链接ctp账户功能
from vnpy_ctp import CtpGateway
# ui界面增加cta策略类功能
from vnpy_ctastrategy import CtaStrategyApp
# ui界面增加cta策略回测功能
from vnpy_ctabacktester import CtaBacktesterApp
# ui界面增加数据管理类功能
from vnpy_datamanager import DataManagerApp
# 策略回测用到的类
from vnpy_ctastrategy.backtesting import BacktestingEngine
```

## 文件

- examples-cta_backtesting    这个文件夹下backtesting_demo是使用notebook进行直接回测的案例

# 数据导入

第一个段是数据收集代码，这里以从金字塔收集数据，然后增加三个vnpy必须的三个字段

```python
from PythonApi import *
import datetime
import pandas as pd
bar_len=100000
bar_close=history_bars('ZJIF00', bar_len, '1m', 
                       ['datetime','open','high','low','close',
                        'volume','total_turnover','open_interest'])
df = pd.DataFrame(bar_close)
df.columns = ['datetime','open','high','low','close',
              'volume','total_turnover','open_interest']
# 这三个字段是vnpy必须格式
df['interval'] = '1m'
df['exchange']= 'CFFEX'
df['symbol'] = 'IF88'

#使用函数
def age_map(x):
    x = str(int(x))
    x = x[:4]+'-'+x[4:6]+'-'+x[6:8]+' '+x[8:10]+':'+x[10:12]+':'+x[12:]
    x = datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S')
    return x
df["datetime"] = df["datetime"].map(age_map)
datetime_format = '%Y%m%d %H:%M:%S'
df['datetime'] = pd.to_datetime(df['datetime'],format=datetime_format)
# 保存csv，不要第一列数字列
df.to_csv('D:/if888.csv', index=None)
```

第二步在.vntrader文件夹的vt_setting.json中添加下面设置这个就表示启用mongodb数据库

```json
 {
 "database.name": "mongodb",
 "database.database": "vnpy",
 "database.host": "127.0.0.1",
 "database.port": 27017,
 "database.user": "",
 "database.password": "",
 "database.driver": "mongodb",
 "database.authentication_source": ""
 }
```

第三步在vnpy中加载前面csv文件，然后通过save_bar_data这个函数可以加到我们的mongodb中

导入也可以通过加载类main_engine.add_app(DataManagerApp)，然后可视化方法导入第一步导出的csv文件，两种方法都可以。

```python
from vnpy.trader.constant import (Exchange, Interval)
import pandas as pd
from vnpy.trader.database import get_database
from vnpy.trader.object import (BarData,TickData)

# 封装函数
def move_df_to_mongodb(imported_data:pd.DataFrame,collection_name:str):
    bars = []
    start = None
    count = 0
    for row in imported_data.itertuples():
        bar = BarData(
              symbol=row.symbol,
              exchange=Exchange(row.exchange),
              datetime=row.datetime,
              interval=Interval(row.interval),
              volume=row.volume,
              open_price=row.open,
              high_price=row.high,
              low_price=row.low,
              close_price=row.close,
              open_interest=row.open_interest,
              gateway_name="DB",
        )
        bars.append(bar)

        # do some statistics
        count += 1
        if not start:
            start = bar.datetime
    end = bar.datetime

    # insert into database
    database_manager = get_database()
    database_manager.save_bar_data(bars, collection_name)
    print(f'Insert Bar: {count} from {start} - {end}')

if __name__ == "__main__":
    # 读取需要入库的csv文件，该文件是用gbk编码
    imported_data = pd.read_csv('./if888.csv',encoding='gbk')
    # datetime格式保存到csv中都会变成object格式，所以这里加载后还需转换回来
    datetime_format = '%Y%m%d %H:%M:%S'
    imported_data['datetime'] = pd.to_datetime(imported_data['datetime'], format=datetime_format)
    move_df_to_mongodb(imported_data,'IF88')
```

# K线生成

在vnpy中k线生成是在每个策略里面自己编写的，通过标准k线合成工具BarGenerator。策略中的on_bar回调函数是把tick数据合成1分钟

on_5min_bar是自己定义好的用1分钟合成N分钟（这里是5分钟）。

```python
class DemoStrategy2(CtaTemplate):
    def __init__(
        self,
        cta_engine: Any,
        strategy_name: str,
        vs_symbol: str,
        setting:dict
    ):
        super().__init__(cta_engine, strategy_name, vs_symbol, setting)
        self.bg = BarGenerator(
            self.on_bar,
            window=5,
            on_window_bar=self.on_5min_bar,
            interval = Interval.MINUTE)
        self.am = ArrayManager()
    def on_bar(self, bar: BarData):
        # k线更新
        self.bg.update_bar(bar)
    def on_5min_bar(self, bar: BarData):
        am = self.am
        am.update_bar(bar)
        if not am.inited:
            return
        # 计算技术指标
        fast_ma = am.sma(self.fast_window, array=True)
        self.fast_ma0 = fast_ma[-1]
        self.fast_ma1 = fast_ma[-2]
```

# 时间序列

上面的BarGenerator生成的是单一的一个k线，ArrayManager是一个k线序列类

我们的策略中每次执行am.update_bar(bar)会给am这个类推进去一个k线bar，然后am中会进行计数count的自增1操作，当累计超过size这个数量时候，我们认为有了足够的k序列数据量把inited置为1，运行执行策略中后面的代码了。

并且在满足size数量后每次更新bar，会把第一根k给丢弃，然后存入最新一根k。

```python
class ArrayManager(object):
    """
    For:
    1. time series container of bar data
    2. calculating technical indicator value
    """

    def __init__(self, size: int = 100) -> None:
        """Constructor"""
        self.count: int = 0
        self.size: int = size
        self.inited: bool = False

        self.open_array: np.ndarray = np.zeros(size)
        self.high_array: np.ndarray = np.zeros(size)
        self.low_array: np.ndarray = np.zeros(size)
        self.close_array: np.ndarray = np.zeros(size)
        self.volume_array: np.ndarray = np.zeros(size)
        self.turnover_array: np.ndarray = np.zeros(size)
        self.open_interest_array: np.ndarray = np.zeros(size)

    def update_bar(self, bar: BarData) -> None:
        """
        Update new bar data into array manager.
        """
        self.count += 1
        if not self.inited and self.count >= self.size:
            self.inited = True

        self.open_array[:-1] = self.open_array[1:]
        self.high_array[:-1] = self.high_array[1:]
        self.low_array[:-1] = self.low_array[1:]
        self.close_array[:-1] = self.close_array[1:]
        self.volume_array[:-1] = self.volume_array[1:]
        self.turnover_array[:-1] = self.turnover_array[1:]
        self.open_interest_array[:-1] = self.open_interest_array[1:]

        self.open_array[-1] = bar.open_price
        self.high_array[-1] = bar.high_price
        self.low_array[-1] = bar.low_price
        self.close_array[-1] = bar.close_price
        self.volume_array[-1] = bar.volume
        self.turnover_array[-1] = bar.turnover
        self.open_interest_array[-1] = bar.open_interest
```
