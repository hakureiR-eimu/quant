import akshare as ak
def get_stock_day_lines(symbol):
    """
    获取单只股票日线数据
    :param symbol: 股票代码，如 "000001"
    """
    try:
        df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date="20200101",adjust="qfq")
        return df
    except Exception as e:
        print(f"获取 {symbol} 数据失败: {e}")
        return None

def get_stock_week_lines(symbol):
    """
    获取单只股票周线数据
    :param symbol: 股票代码，如 "000001"
    """
    try:
        df = ak.stock_zh_a_hist(symbol=symbol, period="weekly", start_date="20200101",adjust="qfq")
        return df
    except Exception as e:
        print(f"获取 {symbol} 数据失败: {e}")
        return None
