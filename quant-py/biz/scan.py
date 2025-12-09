from service.data import get_stock_day_lines,get_stock_week_lines;
SELECTED_STOCKS = [
    {"symbol": "518660", "name": "工银黄金"},
    {"symbol": "601899", "name": "紫金矿业"},
    {"symbol": "517520", "name": "黄金股ETF"},
    {"symbol": "159545", "name": "港股红利"},
    {"symbol": "600938", "name": "中国海油"},
    {"symbol": "600674", "name": "川投能源"},
    {"symbol": "511260", "name": "国债ETF"},
    {"symbol": "002170", "name": "芭田股份"},
    {"symbol": "159696", "name": "纳指ETF"},
]

def run():
    for stock in SELECTED_STOCKS:
        # 日线扫描
        df_day = get_stock_day_lines(stock["symbol"])
        # 月线扫描
        df_week = get_stock_week_lines(stock["symbol"])
    pass