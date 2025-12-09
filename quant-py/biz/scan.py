import time 
import random
from service.data import get_stock_day_lines,get_stock_week_lines;
from service.strategies import super_trend,vegas_tunnel
from service.notification import notify
SELECTED_STOCKS = [
    {"symbol": "518660", "name": "工银黄金"},
    {"symbol": "601899", "name": "紫金矿业"},
    {"symbol": "517520", "name": "黄金股ETF"},
    {"symbol": "159545", "name": "港股红利"},
    {"symbol": "600938", "name": "中国海油"},
    {"symbol": "600674", "name": "川投能源"},
    {"symbol": "159696", "name": "纳指ETF"},
]

def run():
    for stock in SELECTED_STOCKS:
        #   日线扫描
        #   包含列:
        #   日期, 股票代码, 开盘, 收盘, 最高, 最低, 成交量, 成交额, 振幅, 涨跌幅, 涨跌额, 换手率
        df_day = get_stock_day_lines(stock["symbol"])
        if(df_day is None):
            print(f"未获取到{stock['name']}日线数据")
            continue
        else:
            print(df_day.head())
        
        super_trend_signal = super_trend(df_day)
        if super_trend_signal == 1:
            notify(f"日线级别 {stock['name']} 触发 SuperTrend 买入信号")
        elif super_trend_signal == -1:
            notify(f"日线级别 {stock['name']} 触发 SuperTrend 卖出信号")
        if vegas_tunnel(df_day):
            notify(f"日线级别 {stock['name']} 触发 VegasTunnel 信号")
        time.sleep(random.uniform(3, 5))  # 避免请求过快被封IP
        # 周线扫描
        df_week = get_stock_week_lines(stock["symbol"])
        if(df_week is None):
            print(f"未获取到{stock['name']}周线数据")
            continue
        else:
            print(df_week.head())
        
        super_trend_signal = super_trend(df_week)
        if super_trend_signal == 1:
            notify(f"周线级别 {stock['name']} 触发 SuperTrend 买入信号")
        elif super_trend_signal == -1:
            notify(f"周线级别 {stock['name']} 触发 SuperTrend 卖出信号")
        if vegas_tunnel(df_week):
            notify(f"周线级别 {stock['name']} 触发 VegasTunnel 信号")
        time.sleep(random.uniform(3, 5))  # 避免请求过快被封IP