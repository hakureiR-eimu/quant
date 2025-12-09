import ta.trend
import ta.volatility
import pandas as pd


def super_trend(df, period=10, multiplier=3.0):
    """
    SuperTrend 策略
    以3倍ATR作为上下轨，判断趋势
    突破下轨为卖出信号，突破上轨为买入信号
    
    :param df: DataFrame，包含'最高', '最低', '收盘'列
    :param period: ATR周期，默认10
    :param multiplier: ATR乘数，默认3.0
    :return: int, 1=买入信号, -1=卖出信号, 0=无信号
    """
    if df is None or len(df) < period + 1:
        return 0
    
    df = df.copy()
    
    # 1. 计算ATR（使用标准ATR）
    atr_indicator = ta.volatility.AverageTrueRange(
        high=df['最高'],
        low=df['最低'],
        close=df['收盘'],
        window=period
    )
    df['atr'] = atr_indicator.average_true_range()
    
    # 2. 计算价格源 hl2 = (最高 + 最低) / 2
    df['src'] = (df['最高'] + df['最低']) / 2
    
    # 3. 初始化列
    df['up'] = 0.0      # 下支撑线
    df['dn'] = 0.0      # 上阻力线
    df['trend'] = 1     # 趋势：1=上涨, -1=下跌
    
    # 4. 逐行计算 SuperTrend
    for i in range(len(df)):
        # 基础上下轨
        basic_up = df['src'].iloc[i] - (multiplier * df['atr'].iloc[i])
        basic_dn = df['src'].iloc[i] + (multiplier * df['atr'].iloc[i])
        
        if i == 0:
            df.loc[df.index[i], 'up'] = basic_up
            df.loc[df.index[i], 'dn'] = basic_dn
            df.loc[df.index[i], 'trend'] = 1
        else:
            prev_close = df['收盘'].iloc[i-1]
            prev_up = df['up'].iloc[i-1]
            prev_dn = df['dn'].iloc[i-1]
            prev_trend = df['trend'].iloc[i-1]
            
            # 计算 up（下支撑线）
            # Pine Script: up := close[1] > up1 ? max(up, up1) : up
            if prev_close > prev_up:
                current_up = max(basic_up, prev_up)
            else:
                current_up = basic_up
            df.loc[df.index[i], 'up'] = current_up
            
            # 计算 dn（上阻力线）
            # Pine Script: dn := close[1] < dn1 ? min(dn, dn1) : dn
            if prev_close < prev_dn:
                current_dn = min(basic_dn, prev_dn)
            else:
                current_dn = basic_dn
            df.loc[df.index[i], 'dn'] = current_dn
            
            # 计算趋势
            # Pine Script: trend := trend == -1 and close > dn1 ? 1 : 
            #                      trend == 1 and close < up1 ? -1 : trend
            current_close = df['收盘'].iloc[i]
            
            if prev_trend == -1 and current_close > prev_dn:
                current_trend = 1
            elif prev_trend == 1 and current_close < prev_up:
                current_trend = -1
            else:
                current_trend = prev_trend
            
            df.loc[df.index[i], 'trend'] = current_trend
    
    # 5. 判断信号
    if len(df) < 2:
        return 0
    
    current_trend = df['trend'].iloc[-1]
    prev_trend = df['trend'].iloc[-2]
    
    # 从 -1 转为 1：买入信号
    if prev_trend == -1 and current_trend == 1:
        return 1
    # 从 1 转为 -1：卖出信号
    elif prev_trend == 1 and current_trend == -1:
        return -1
    # 无变化：无信号
    else:
        return 0


def vegas_tunnel(df):
    """
    维加斯通道
    条件：
    1. 144EMA在169EMA上方
    2. 收盘价上穿144EMA（当前收盘价>144EMA 且 前一收盘价<=144EMA）
    
    :param df: DataFrame，需包含'收盘'列
    :return: bool，是否满足条件
    """
    if df is None or len(df) < 170:  # 需要至少170条数据（169+1用于判断上穿）
        return False
    
    # 计算EMA
    ema144 = ta.trend.EMAIndicator(df['收盘'], window=144).ema_indicator()
    ema169 = ta.trend.EMAIndicator(df['收盘'], window=169).ema_indicator()
    
    # 获取最新值
    latest_close = df['收盘'].iloc[-1]
    prev_close = df['收盘'].iloc[-2]
    latest_ema144 = ema144.iloc[-1]
    prev_ema144 = ema144.iloc[-2]
    latest_ema169 = ema169.iloc[-1]
    
    # 判断条件
    ema144_above_ema169 = latest_ema144 > latest_ema169
    
    # 上穿：当前收盘价 > 144EMA 且 前一收盘价 <= 前一144EMA
    cross_above = latest_close > latest_ema144 and prev_close <= prev_ema144
    
    return ema144_above_ema169 and cross_above