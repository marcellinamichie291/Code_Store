import talib
import numpy as np
# 各种均线
def any_ma(close,key='sma'):
    if key.lower() == 'sma':
        # ma简单移动平均
        result = talib.SMA(close, 10)
    elif key.lower() == 'ema':
        # ema指数移动指标
        result = talib.EMA(close, 10)
    elif key.lower() == 'wma':
        # wma加权移动平均
        result = talib.WMA(close, 10)
    else:
        result = 0
    return result
# 1.DIFF、DEA均为正，DIFF向上突破DEA，买入信号
# 2.DIFF、DEA均为负，DIFF向下跌破DEA，卖出信号
# 3.DEA线与K线发生背离，行情反转信号
# 4.分析MACD柱状线，由红变绿(正变负)，卖出信号；由绿变红，买入信号
def macd(close):
    # 参数:fastperiod和slowperiod是ema快线和慢线的对应周期，signalperiod是快慢线差值dea的周期
    # 返回值:三个返回值具体看图表上的指标，注意talib中返回的macd是(DIF-DEA)，而国内软件都会乘以2，所以我们在使用时候需要自己*2来使得数值一样
    dif, dea, macd = talib.MACD(close,fastperiod=12,slowperiod=26,signalperiod=9)
    # 返回序列
    return dif,dea,macd
# 1.股价上升穿越布林线上限时，回档机率大
# 2.股价下跌穿越布林线下限时，反弹机率大
# 3.布林线震动波带变窄时，表示变盘在即
# 4.BOLL须配合BB 、WIDTH 使用
def boll(close):
    # 注意：talib中计算的标准差算法用的是stdp总体标准差，然国内软件里用的是std样本标准差。区别就是前者除以样本总数，后者除以样本总数 - 1
    # 所以如果想要自己实现和图表一样的布林线值只能自己写了，其中std的算法参考我后面的例子
    # 这里给出两种标准差的python实现，如果想自己实现国内的那种标准差就用std这个。
    mean = np.array(close).mean()
    stdp = np.sqrt((1 / (len(close))) * np.sum((np.array(close) - mean) ** 2))
    std = np.sqrt((1 / (len(close) - 1)) * np.sum((np.array(close) - mean) ** 2))
    # timeperiod表示均线的周期，nbdevup表示上轨几个标准差，nbdevdn表示下跪几个标准差，matype=0表示用ma计算均线，matype=1表示用ema计算均线
    upper, mid, lower = talib.BBANDS(close, timeperiod=26, nbdevup=2, nbdevdn=2, matype=0)
    return upper, mid, lower
# 抛物转向
def sar(high,low):
    # acceleration表示步长，maximum表示极限值
    sar = talib.SAR(high, low, acceleration=0.02, maximum=0.2)
    return sar
# 1.RSI>80 为超买，RSI<20 为超卖
# 2.RSI 以50为中界线，大于50视为多头行情，小于50视为空头行情
# 3.RSI 在80以上形成Ｍ头或头肩顶形态时，视为向下反转信号
# 4.RSI 在20以下形成Ｗ底或头肩底形态时，视为向上反转信号
# 5.RSI 向上突破其高点连线时，买进
# 6.RSI 向下跌破其低点连线时，卖出
def rsi(close):
    # 就一个周期参数就行了
    rsi = talib.RSI(close, timeperiod=6)
    return rsi
# WR波动于0 - 100，100置于顶部，0置于底部。
# 本指标以50为中轴线，高于50视为股价转强；低于50视为股价转弱
# 本指标高于20后再度向下跌破20，卖出；低于80后再度向上突破80，买进。
# WR连续触底3 - 4次，股价向下反转机率大；连续触顶3 - 4次，股价向上反转机率大。
def wr(close,high,low):
    wr = talib.WILLR(high, low, close, timeperiod=14)
    return wr
# 1.TRIX由下往上交叉其平均线时，为长期买进信号
# 2.TRIX由上往下交叉其平均线时，为长期卖出信号
# 3.DMA、MACD、TRIX 三者构成一组指标群，互相验证。
def trix(close):
    trix = talib.TRIX(close, timeperiod=12)
    mean = talib.SMA(trix, 20)
    return trix,mean
# TR真实波幅
def tr(close,high,low):
    tr = talib.TRANGE(high, low, close)
    mean = talib.SMA(tr, 14)
    return tr,mean
# 1.指标>80 时，回档机率大；指标<20时，反弹机率大
# 2.K在20左右向上交叉D时，视为买进信号
# 3.K在80左右向下交叉D时，视为卖出信号
# 4.J>100 时，股价易反转下跌；J<0 时，股价易反转上涨
# 5.KDJ 波动于50左右的任何信号，其作用不大
def kdj(close,high,low):
    # talib中算法matype=0用的是简单平均，国内软件都用的是sma计算，所以会有出入
    k, d = talib.STOCH(high, low, close, fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    j = 3 * k - 2 * d
    return k,d,j
