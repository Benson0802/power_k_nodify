import shioaji as sj
from shioaji import TickFOPv1, Exchange
import threading
from check_opening import check_opening
import json
from convertK import convertK
import datetime
import globals
import pandas as pd
import math
import requests
import logging
import csv
import time

globals.initialize()
obj = check_opening()
year_mon = obj.get_year_mon()
globals.code = 'TXF' + str(year_mon['year']) + ('0' if len(str(year_mon['mon'])) == 1 else '') + str(year_mon['mon'])

def power_kbar(tick_close):
    '''
     能量K棒計算
    '''
    print('能量k棒計算')
    df_1Min = pd.read_csv('data/1Min.csv').iloc[-1]
    df_5Min = pd.read_csv('data/5Min.csv').iloc[-1]
    df_15Min = pd.read_csv('data/15Min.csv').iloc[-1]
    df_30Min = pd.read_csv('data/30Min.csv').iloc[-1]
    
    df_d = None
    df_1k = pd.read_csv('data/1Min.csv',index_col='datetime')
    df_1k.index = pd.to_datetime(df_1k.index, format="%Y-%m-%d %H:%M:%S", errors='coerce')    
    current_time = datetime.datetime.now()
    d_start_time = current_time.replace(hour=8, minute=45, second=0, microsecond=0)
    d_end_time = current_time.replace(hour=13, minute=45, second=0, microsecond=0)
    n_start_time = current_time.replace(hour=15, minute=0, second=0, microsecond=0)
    n_end_time = (current_time + datetime.timedelta(days=1)).replace(hour=5, minute=0, second=0, microsecond=0)
    if d_start_time < current_time < d_end_time:
        df_between_time_morning = df_1k.between_time('15:01', '23:59', inclusive='left')
        df_between_time_night = df_1k.between_time('00:00', '05:00', inclusive='left')
        df_combined = pd.concat([df_between_time_morning, df_between_time_night])
        df_d = df_combined.resample('D').apply({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }).dropna()
        if df_d.iloc[-1]['close'] > df_d.iloc[-1]['open']:
            print("日k紅")
            globals.day_color = "r"
        else:
            print("日k綠")
            globals.day_color = "g"
    elif n_start_time < current_time < n_end_time:
        df_d = df_1k.between_time('08:46', '13:45').resample('D').apply({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }).dropna()
        if df_d.iloc[-1]['close'] > df_d.iloc[-1]['open']:
            print("日k紅")
            globals.day_color = "r"
        else:
            print("日k綠")
            globals.day_color = "g"
    else:
        print("現在時間不在任何時間範圍內。")
    
    if df_1Min['volume'] >= 1000:
        get_power_data(1, tick_close, df_1Min)
    # if df_5Min['volume'] >= 1000:
    #     get_power_data(5, tick_close, df_5Min)
    # elif df_15Min['volume'] >= 1000:
    #     get_power_data(15, tick_close, df_15Min)
    # elif df_30Min['volume'] >= 1000:
    #     get_power_data(30, tick_close, df_30Min)
    
    # df_15Min = pd.read_csv('data/15Min.csv').iloc[-2]
    # df_30Min = pd.read_csv('data/30Min.csv').iloc[-2]
    # df_kbar = pd.read_csv('data/kbar.csv')
    # df_1_kbar = None
    # df_5_kbar = None
    # df_15_kbar = None
    # df_30_kbar = None

    # try:
    #     df_1_kbar = df_kbar[df_kbar['minute'].values == 1].tail(1)
    # except IndexError:
    #     df_1_kbar = None
        
    # try:
    #     df_5_kbar = df_kbar[df_kbar['minute'].values == 5].tail(1)
    # except IndexError:
    #     df_5_kbar = None
        
    # try:
    #     df_15_kbar = df_kbar[df_kbar['minute'].values == 15].tail(1)
    # except IndexError:
    #     df_15_kbar = None
        
    # try:
    #     df_30_kbar = df_kbar[df_kbar['minute'].values == 30].tail(1)
    # except IndexError:
    #     df_30_kbar = None
    
    # if df_1_kbar is None or df_1_kbar.empty:
    #     if df_1Min['volume'] >= 1000:
    #         get_power_data(1, tick_close, df_1Min)
    # else:
    #     df_1_kbar['datetime'] = df_1_kbar['datetime'].astype(str)
    #     if df_1_kbar['datetime'].values[0] != df_1Min['datetime']:
    #         if df_1Min['volume'] >= 1000:
    #             get_power_data(1, tick_close, df_1Min)
                
    # if df_5_kbar is None or df_5_kbar.empty:
    #     if df_5Min['volume'] >= 1000:
    #         get_power_data(5, tick_close, df_5Min)
    # else:
    #     df_5_kbar['datetime'] = df_5_kbar['datetime'].astype(str)
    #     if df_5_kbar['datetime'].values[0] != df_5Min['datetime']:
    #         if df_5Min['volume'] >= 1000:
    #             get_power_data(5, tick_close, df_5Min)
            
    # if df_15_kbar is None or df_15_kbar.empty:
    #     if df_15Min['volume'] >= 1000:
    #         get_power_data(15, tick_close, df_15Min)
    # else:
    #     df_15_kbar['datetime'] = df_15_kbar['datetime'].astype(str)
    #     if df_15_kbar['datetime'].values[0] != df_15Min['datetime']:
    #         if df_15Min['volume'] >= 1000:
    #             get_power_data(15, tick_close, df_15Min)
    
    # if df_30_kbar is None or df_30_kbar.empty:
    #     if df_30Min['volume'] >= 1000:
    #         get_power_data(30, tick_close, df_30Min)
    # else:
    #     df_30_kbar['datetime'] = df_30_kbar['datetime'].astype(str)
    #     if df_30_kbar['datetime'].values[0] != df_30Min['datetime']:
    #         if df_30Min['volume'] >= 1000:
    #             get_power_data(30, tick_close, df_30Min)

    # trade(int(tick_close),datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),0)

def get_power_data(minute,tick_close,df):
    volume = float(str(df['volume'])[0] + '.' + str(df['volume'])[1:]) if int(
        str(df['volume'])[0]) < 6 else float('0.' + str(df['volume']))
    color = None
    datetime = df['datetime']
    power = math.floor((df['high'] - df['low']) * volume)
    hh = math.ceil(df['high'] + power)
    h = math.ceil(df['close'] + power)
    l = math.ceil(df['close'] - power)
    ll = math.ceil(df['low'] - power)
    op_h = math.ceil(df['low'] + power)
    op_l = math.ceil(df['high'] - power)
    if df['close'] >= df['open']:
        color = 'K：紅'
    else:
        color = 'k：綠'
    
    df_kbar = pd.read_csv('data/kbar.csv')
    if df_kbar.empty:
        trade(int(tick_close),datetime,minute)
        lineMsgFormat(minute,datetime,'',color,df['close'],df['volume'],power,hh,h,l,ll,op_h,op_l,tick_close)
    else:
        df_5kbar = df_kbar.tail(1)
        tmp_datetime = pd.to_datetime(datetime)
        if str(tmp_datetime) != df_5kbar['datetime'].values[0]:
            maturity_time = tmp_datetime + pd.Timedelta(minutes=power)
            trade(int(tick_close),datetime,minute)
            lineMsgFormat(minute,datetime,maturity_time,color,df['close'],df['volume'],power,hh,h,l,ll,op_h,op_l,tick_close)

def trade(close,kbar_datetime,minute):
    '''
    交易
    '''
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
    df_trade = pd.read_csv('data/trade.csv', index_col='datetime')
    loss = 10  # 損失幾點出場
    balance = 0  # 賺or賠 計算方式 => ((賣出部位-收盤部位)*50)-70手續費
    total_balance = df_trade['balance'].sum()  # 總賺賠
    has_order = False
    if not df_trade.empty:
        if df_trade.iloc[-1]['type'] == 1:
            has_order = True
    df_kbar = pd.read_csv('data/kbar.csv')
    df_5 = df_kbar.tail(1)
    # df_kbar = pd.read_csv('data/kbar.csv')
    # df_1 = df_kbar[df_kbar['minute'] == 1].tail(1)
    # df_5 = df_kbar[df_kbar['minute'] == 5].tail(1)
    # df_15 = df_kbar[df_kbar['minute'] == 15].tail(1)
    # df_30 = df_kbar[df_kbar['minute'] == 30].tail(1)
    # min1_maturity_time = None
    # min5_maturity_time = None
    # min15_maturity_time = None
    # min30_maturity_time = None
    
    # if df_1['maturity_time'].any() and minute == 1:
    #     min1_maturity_time = pd.to_datetime(df_1['maturity_time'], format="%H:%M").iloc[0].time()
    #     min1_maturity_time = datetime.time(hour=min1_maturity_time.hour, minute=min1_maturity_time.minute, second=0)
    # if df_5['maturity_time'].any() and minute == 5:
    #     min5_maturity_time = pd.to_datetime(df_5['maturity_time'], format="%H:%M").iloc[0].time()
    #     min5_maturity_time = datetime.time(hour=min5_maturity_time.hour, minute=min5_maturity_time.minute, second=0)
    # if df_15['maturity_time'].any() and minute == 15:
    #     min15_maturity_time = pd.to_datetime(df_15['maturity_time'], format="%H:%M").iloc[0].time()
    #     min15_maturity_time = datetime.time(hour=min15_maturity_time.hour, minute=min15_maturity_time.minute, second=0)
    # if df_30['maturity_time'].any() and minute == 30:
    #     min30_maturity_time = pd.to_datetime(df_30['maturity_time'], format="%H:%M").iloc[0].time()
    #     min30_maturity_time = datetime.time(hour=min30_maturity_time.hour, minute=min30_maturity_time.minute, second=0)
        
    # now_min = datetime.datetime.now().replace(second=0, microsecond=0).time()
    
    if has_order == False and minute != 0:# 目前沒單
        # if min1_maturity_time is not None:
        #     if now_min <= min1_maturity_time:
        #         if close >= df_1['op_h'].values[0]:
        #             logging.info("1分k買進空單 close:"+str(close)+" op_h:"+str(df_1['op_h'].values[0]))
        #             print('買進空單')
        #             buy_sell(1, -1, close, balance,total_balance,1,kbar_datetime)  # 買進空單
        #         elif close <= df_1['op_l'].values[0]:
        #             logging.info("1分k買進多單 close:"+str(close)+" op_l:"+str(df_1['op_l'].values[0]))
        #             print('買進多單')
        #             buy_sell(1, 1, close, balance,total_balance,1,kbar_datetime)  # 買進多單
        # elif min5_maturity_time is not None:
        # if min5_maturity_time is not None:
        #     if now_min <= min5_maturity_time:
        #         if close >= df_5['op_h'].values[0]:
        #             logging.info("5分k買進空單 close:"+str(close)+" op_h:"+str(df_5['op_h'].values[0]))
        #             print('買進空單')
        #             buy_sell(1, -1, close, balance,total_balance,5,kbar_datetime)  # 買進空單
        #         elif close <= df_5['op_l'].values[0]:
        #             logging.info("5分k買進多單 close:"+str(close)+" op_l:"+str(df_5['op_l'].values[0]))
        #             print('買進多單')
        #             buy_sell(1, 1, close, balance,total_balance,5,kbar_datetime)  # 買進多單
        # elif min15_maturity_time is not None:
        #     if now_min <= min15_maturity_time:
        #         if close >= df_15['op_h'].values[0]:
        #             logging.info("15分k買進空單 close:"+str(close)+" op_h:"+str(df_15['op_h'].values[0]))
        #             buy_sell(1, -1, close, balance,total_balance,15,kbar_datetime)  # 買進空單
        #         elif close <= df_15['op_l'].values[0]:
        #             logging.info("15分k買進多單 close:"+str(close)+" op_l:"+str(df_15['op_l'].values[0]))
        #             print('買進多單')
        #             buy_sell(1, 1, close, balance,total_balance,15,kbar_datetime)  # 買進多單
        # elif min30_maturity_time is not None:
        #     if now_min <= min30_maturity_time:
        #         if close >= df_30['op_h'].values[0]:
        #             logging.info("30分k買進空單 close:"+str(close)+" op_h:"+str(df_30['op_h'].values[0]))
        #             buy_sell(1, -1, close, balance,total_balance,30,kbar_datetime)  # 買進空單
        #         elif close <= df_30['op_l'].values[0]:
        #             logging.info("30分k買進多單 close:"+str(close)+" op_l:"+str(df_30['op_l'].values[0]))
        #             print('買進多單')
        #             buy_sell(1, 1, close, balance,total_balance,30,kbar_datetime)  # 買進多單
        
        # 依日k紅棒做低點
        if not df_5.empty:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if globals.day_color == "r":
                if close <= df_5['l'].values[0]:
                    logging.info("現在時間:"+now+" 參考的5分k時間"+df_5['datetime']+" 5分k買進多單 現價:"+str(close)+" 低:"+str(df_5['l'].values[0]))
                    print('買進多單')
                    buy_sell(1, 1, close, balance,total_balance,5,kbar_datetime)  # 買進多單
            elif globals.day_color == "g":
                if close >= df_5['h'].values[0]:
                    logging.info("現在時間:"+now+" 參考的5分k時間"+df_5['datetime']+" 5分k買進空單 現價:"+str(close)+" 高:"+str(df_5['h'].values[0]))
                    print('買進空單')
                    buy_sell(1, -1, close, balance,total_balance,5,kbar_datetime)  # 買進空單
        # if not df_5.empty:
        #     if close >= df_5['op_h'].values[0]:
        #         logging.info("5分k買進空單 close:"+str(close)+" op_h:"+str(df_5['op_h'].values[0]))
        #         print('買進空單')
        #         buy_sell(1, -1, close, balance,total_balance,5,kbar_datetime)  # 買進空單
        #     elif close <= df_5['op_l'].values[0]:
        #         logging.info("5分k買進多單 close:"+str(close)+" op_l:"+str(df_5['op_l'].values[0]))
        #         print('買進多單')
        #         buy_sell(1, 1, close, balance,total_balance,5,kbar_datetime)  # 買進多單
            
    else:# 目前有單 
        if len(df_trade) > 0:
            close = int(close)
            loss = int(loss)
            price = int(df_trade['price'].iloc[-1])
            if df_trade['type'].iloc[-1] == 1:  # 有單時
                if df_trade['lot'].iloc[-1]  == 1:  # 有多單的處理
                    #判斷是幾分k通知的單
                    # if df_trade['minute'].iloc[-1] == 1:
                    #     if close <= (price  - loss):
                    #         logging.info("1分k多單停損 close:"+str(close)+" price:"+str(price)+" loss:"+str(loss))
                    #         logging.info("1分k多單停損算錢 close:"+str(close)+" price:"+str(price)+" 算出來的結果:"+str(((close - price )*50)-70))
                    #         balance = ((close - price )*50)-70
                    #         print('多單停損')
                    #         buy_sell(-1, -1, close, balance,total_balance,1,kbar_datetime)
                    #     elif close >= df_1['op_h'].values[0]:
                    #         logging.info("1分k多單停利 close:"+str(close)+" op_h:"+str(df_1['op_h'].values[0]))
                    #         logging.info("1分k多單停利算錢 close:"+str(close)+" price:"+str(price)+" 算出來的結果:"+str( ((close - price )*50)-70))
                    #         balance = ((close - price )*50)-70  # 計算賺賠
                    #         print('多單停利')
                    #         buy_sell(-1, -1,close, balance,total_balance,1,kbar_datetime)  # 多單停利
                    # elif df_trade['minute'].iloc[-1] == 5:
                    
                    #依日k紅棒及5分k的能+低的判斷出場
                    if df_trade['minute'].iloc[-1] == 5:
                        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if close >= (df_5['l'].values[0] + df_5['power'].values[0]):
                            logging.info("現在時間:"+now+" 參考的5分k時間"+df_5['datetime']+" 多單停利 現價:"+str(close)+" 滿足點:"+str(df_5['l'].values[0] + df_5['power'].values[0]))
                            balance = ((close - price )*50)-70  # 計算賺賠
                            print('多單停利')
                            buy_sell(-1, -1,close, balance,total_balance,5,kbar_datetime)  # 多單停利
                        if close <= (df_5['l'].values[0] - 10):
                            logging.info("現在時間:"+now+" 參考的5分k時間"+df_5['datetime']+" 多單停損 現價:"+str(close)+" 停損點:"+str(close - price))
                            balance = ((close - price )*50)-70
                            print('多單停損')
                            buy_sell(-1, -1, close, balance,total_balance,5,kbar_datetime)
                    # if df_trade['minute'].iloc[-1] == 5:
                    #     if close <= (price  - loss):
                    #         logging.info("5分k多單停損 close:"+str(close)+" price:"+str(price)+" loss:"+str(loss))
                    #         logging.info("5分k多單停損算錢 close:"+str(close)+" price:"+str(price)+" 算出來的結果:"+str(((close - price )*50)-70))
                    #         balance = ((close - price )*50)-70
                    #         print('多單停損')
                    #         buy_sell(-1, -1, close, balance,total_balance,5,kbar_datetime)
                    #     elif close >= df_5['op_h'].values[0]:
                    #         logging.info("5分k多單停利 close:"+str(close)+" op_h:"+str(df_5['op_h'].values[0]))
                    #         logging.info("5分k多單停利算錢 close:"+str(close)+" price:"+str(price)+" 算出來的結果:"+str( ((close - price )*50)-70))
                    #         balance = ((close - price )*50)-70  # 計算賺賠
                    #         print('多單停利')
                    #         buy_sell(-1, -1,close, balance,total_balance,5,kbar_datetime)  # 多單停利
                            
                    # elif df_trade['minute'].iloc[-1] == 15:
                    #     if close <= (price  - loss):
                    #         logging.info("15分k多單停損 close:"+str(close)+" price:"+str(price)+" loss:"+str(loss))
                    #         logging.info("15分k多單停損算錢 close:"+str(close)+" price:"+str(price)+" 算出來的結果:"+str(((close - price )*50)-70))
                    #         balance = ((close - price )*50)-70
                    #         print('多單停損')
                    #         buy_sell(-1, -1, close, balance,total_balance,15,kbar_datetime)
                    #     elif close >= df_15['op_h'].values[0]:
                    #         logging.info("15分k多單停利 close:"+str(close)+" op_h:"+str(df_15['op_h'].values[0]))
                    #         logging.info("15分k多單停利算錢 close:"+str(close)+" price:"+str(price)+" 算出來的結果:"+str( ((close - price )*50)-70))
                    #         balance = ((close - price )*50)-70  # 計算賺賠
                    #         print('多單停利')
                    #         buy_sell(-1, -1,close, balance,total_balance,15,kbar_datetime)  # 多單停利
                    # elif df_trade['minute'].iloc[-1] == 30:
                    #     if close <= (price  - loss):
                    #         logging.info("30分k多單停損 balance:"+str(balance)+" close:"+str(close)+" loss:"+str(loss))
                    #         logging.info("30分k多單停損算錢 close:"+str(close)+" price:"+str(price)+" 算出來的結果:"+str(((close - price )*50)-70))
                    #         balance = ((close - price )*50)-70
                    #         print('多單停損')
                    #         buy_sell(-1, -1, close, balance,total_balance,30,kbar_datetime)
                    #     elif close >= df_30['op_h'].values[0]:
                    #         logging.info("30分k多單停利 close:"+str(close)+" op_h:"+str(df_30['op_h'].values[0]))
                    #         logging.info("30分k多單停利算錢 close:"+str(close)+" price:"+str(price)+" 算出來的結果:"+str( ((close - price )*50)-70))
                    #         balance = ((close - price )*50)-70  # 計算賺賠
                    #         print('多單停利')
                    #         buy_sell(-1, -1,close, balance,total_balance,30,kbar_datetime)  # 多單停利
                elif df_trade['lot'].iloc[-1]  == -1:  # 空單的處理
                    if df_trade['minute'].iloc[-1] == 5:
                        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if close >= (price + loss):
                            logging.info("現在時間:"+now+" 參考的5分k時間"+str(df_5['datetime'])+" 空單停利 現價:"+str(close)+" 滿足點:"+str(price + loss))
                            balance = ((close - price )*50)-70  # 計算賺賠
                            print('空單停利')
                            buy_sell(-1, 1, close, balance,total_balance,1,kbar_datetime)  # 空單回補
                        if close <= (df_5['h'].values[0] - 10):
                            logging.info("現在時間:"+now+" 參考的5分k時間"+str(df_5['datetime'])+" 空單停損 現價:"+str(close)+" 停損點:"+str(df_5['h'].values[0] - 10))
                            balance = ((close - price )*50)-70
                            print('空單停損')
                            buy_sell(-1, -1, close, balance,total_balance,5,kbar_datetime)
                    # if df_trade['minute'].iloc[-1] == 1:
                    #     if (close >= (price + loss)):
                    #         logging.info("1分k空單回補 close:"+str(close)+" price:"+str(price)+" loss:"+str(loss))
                    #         logging.info("1分k空單回補算錢 close:"+str(close)+" price:"+str(price)+" 算出來的結果:"+str(((close - price )*50)-70))
                    #         balance = ((price - close)*50)-70  # 計算賺賠
                    #         print('空單回補')
                    #         buy_sell(-1, 1, close, balance,total_balance,1,kbar_datetime)  # 空單回補
                    #     elif close <= df_1['op_l'].values[0]:
                    #         logging.info("1分k空單停利 close:"+str(close)+" op_l:"+str(df_1['op_l'].values[0]))
                    #         logging.info("1分k多單停利算錢 close:"+str(close)+" price:"+str(price)+" 算出來的結果:"+str( ((close - price )*50)-70))
                    #         balance = ((price - close)*50)-70  # 計算賺賠
                    #         print('空單停利')
                    #         buy_sell(-1, 1, close, balance,total_balance,1,kbar_datetime)  # 空單停利
                    # elif df_trade['minute'].iloc[-1] == 5:
                    #先不做空單
                    # if df_trade['minute'].iloc[-1] == 5:
                    #     if (close >= (price + loss)):
                    #         logging.info("5分k空單回補 close:"+str(close)+" price:"+str(price)+" loss:"+str(loss))
                    #         logging.info("5分k空單回補算錢 close:"+str(close)+" price:"+str(price)+" 算出來的結果:"+str(((close - price )*50)-70))
                    #         balance = ((price - close)*50)-70  # 計算賺賠
                    #         print('空單回補')
                    #         buy_sell(-1, 1, close, balance,total_balance,5,kbar_datetime)  # 空單回補
                    #     elif close <= df_5['op_l'].values[0]:
                    #         logging.info("5分k空單停利 close:"+str(close)+" op_l:"+str(df_5['op_l'].values[0]))
                    #         logging.info("5分k多單停利算錢 close:"+str(close)+" price:"+str(price)+" 算出來的結果:"+str( ((close - price )*50)-70))
                    #         balance = ((price  - close)*50)-70  # 計算賺賠
                    #         print('空單停利')
                    #         buy_sell(-1, 1, close, balance,total_balance,5,kbar_datetime)  # 空單停利
                    
                    # elif df_trade['minute'].iloc[-1] == 15:
                    #     if (close >= (price + loss)):
                    #         logging.info("15分k空單回補 close:"+str(close)+" price:"+str(price)+" loss:"+str(loss))
                    #         logging.info("15分k空單回補算錢 close:"+str(close)+" price:"+str(price)+" 算出來的結果:"+str(((close - price )*50)-70))
                    #         balance = ((price - close)*50)-70  # 計算賺賠
                    #         print('空單回補')
                    #         buy_sell(-1, 1, close, balance,total_balance,15,kbar_datetime)  # 空單回補
                    #     elif close <= df_15['op_l'].values[0]:
                    #         logging.info("15分k空單停利 close:"+str(close)+" op_l:"+str(df_15['op_l'].values[0]))
                    #         logging.info("15分k多單停利算錢 close:"+str(close)+" price:"+str(price)+" 算出來的結果:"+str( ((close - price )*50)-70))
                    #         balance = ((price - close)*50)-70  # 計算賺賠
                    #         print('空單停利')
                    #         buy_sell(-1, 1, close, balance,total_balance,15,kbar_datetime)  # 空單停利
                    # elif df_trade['minute'].iloc[-1] == 30:
                    #     if (close >= (price + loss)):
                    #         logging.info("30分k空單回補 close:"+str(close)+" price:"+str(price)+" loss:"+str(loss))
                    #         logging.info("30分k空單回補算錢 close:"+str(close)+" price:"+str(price)+" 算出來的結果:"+str(((close - price )*50)-70))
                    #         balance = ((price - close)*50)-70  # 計算賺賠
                    #         print('空單回補')
                    #         buy_sell(-1, 1, close, balance,total_balance,30,kbar_datetime)  # 空單回補
                    #     elif close <= df_30['op_l'].values[0]:
                    #         logging.info("30分k空單停利 close:"+str(close)+" op_l:"+str(df_30['op_l'].values[0]))
                    #         logging.info("30分k多單停利算錢 close:"+str(close)+" price:"+str(price)+" 算出來的結果:"+str( ((close - price )*50)-70))
                    #         balance = ((price  - close)*50)-70  # 計算賺賠
                    #         print('空單停利')
                    #         buy_sell(-1, 1, close, balance,total_balance,30,kbar_datetime)  # 空單停利

def buy_sell(type,lot,close,balance,total_balance,minute,dt):
    '''
    買/回補 or 賣或放空
    type 1:進場 -1:出場
    lot 1:買 -1:賣
    '''
    if type == 1 and lot == 1:
        print('買多')
        total_lot = 1
    elif type == 1 and lot == -1:
        print('放空')
        total_lot = 1
    elif type == -1 and lot == 1:
        print('空單回補')
        total_lot = 0
    elif type == -1 and lot == -1:
        print('多單賣出')
        total_lot = 0
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_balance = total_balance + balance
    with open('data/trade.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([now, type, close, lot, total_lot, balance, total_balance,0,minute,dt])
        lineMsgFormat_trade(now, type, close, lot, total_lot, balance, total_balance)
    
def lineMsgFormat_trade(datetime,type,price,lot,total_lot,balance,total_balance):
    '''
    串接line訊息
    '''
    msg = datetime+' | '
    if type == 1:
        msg += '買'
    if type == -1:
        msg += '賣'
    if lot == 1:
        msg += '進'
    if lot == -1 :
        msg += '出'
    msg += ' | '+str(price)
    if total_lot == 0:
        msg += ' 平倉 | 收入:'
        msg += str(balance)    
        msg += ' | 總盈餘:'
        msg += str(total_balance)
        
    sendMessage(msg)

def lineMsgFormat(minute,datetime,maturity_time,color,close,volume,power,hh,h,l,ll,op_h,op_l,tick_close):
    '''
    能量k的line通知
    '''
    if maturity_time != '':
        maturity_time = str(maturity_time)
        maturity_date , maturity_time = maturity_time.split(" ")
        maturity_time = maturity_time[:-3]
    date, time = datetime.split(" ")
    time = time[:-3]
    day_color = ""
    if globals.day_color != None:
        if globals.day_color == "r":
            day_color = "紅"
        elif globals.day_color == "g":
           day_color = "綠"
    msg = "\n頻率："+str(minute)+'分鐘圖\n'
    msg += "日期："+str(date)+"\n"
    msg += "時間："+str(time)+"\n"
    msg += "時效："+str(maturity_time)+"\n"
    msg += "台股指數近月\n"
    msg += "日k顏色"+str(day_color)+"\n"
    msg += color+"\n"
    msg += "收："+str(close)+"\n"
    msg += "量："+str(volume)+"\n"
    msg += "能："+str(power)+"\n"
    msg += "頂："+str(hh)+"\n"
    msg += "高："+str(h)+"\n"
    msg += "低："+str(l)+"\n"
    msg += "底："+str(ll)+"\n"
    msg += "反轉高點："+str(op_h)+"\n"
    msg += "反轉低點："+str(op_l)+"\n"
    msg += "現價："+str(tick_close)+"\n"
    
    with open('data/kbar.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime, minute, maturity_time, op_h, op_l,h,l,power])
        
    sendMessage(msg)

def sendMessage(message):
    for row in globals.line_token:
        if row != '':
            headers = { "Authorization": "Bearer " + row }
            data = { 'message': message }
            requests.post("https://notify-api.line.me/api/notify",headers = headers, data = data)


with open('API_KEY.json', 'r') as f:
    json_data = json.load(f)
    globals.line_token.append(json_data['line_token1'])
    globals.line_token.append(json_data['line_token2'])
    globals.line_token.append(json_data['line_token3'])
    globals.line_token.append(json_data['line_token4'])
    globals.line_token.append(json_data['line_token5'])
    globals.line_token.append(json_data['line_token6'])
    globals.line_token.append(json_data['line_token7'])
    globals.line_token.append(json_data['line_token8'])
    globals.line_token.append(json_data['line_token9'])
    globals.line_token.append(json_data['line_token10'])

    api = sj.Shioaji()
    api.login(
        api_key=json_data['api_key'],
        secret_key=json_data['secret_key'],
        contracts_cb=lambda security_type: print(f"{repr(security_type)} fetch done.")
    )
    
    # while (True):
    #     #改抓kbar
    #     current_time = datetime.datetime.now()
    #     start_time = current_time.replace(hour=8, minute=45)
    #     end_time = current_time.replace(hour=13, minute=45)
    #     next_day_time = current_time.replace(hour=5, minute=0) + datetime.timedelta(days=1)
    #     if start_time <= current_time <= end_time or current_time >= current_time.replace(hour=15, minute=0) or current_time <= next_day_time:
    #         globals.today = datetime.datetime.now().date().strftime('%Y-%m-%d')
    #         logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
    #         logging.info(current_time)
    #         kbars = api.kbars(
    #             contract=api.Contracts.Futures.TXF.TXFR1,
    #             start=globals.today,
    #             end=globals.today,
    #             timeout = 30000
    #         )
            
    #         ck = convertK(kbars)
    #         ck.write_history_1k_bar()
    #         ck.convert_k_bar('5Min')
    #         ck.convert_k_bar('15Min')
    #         ck.convert_k_bar('30Min')
    #         # ck.convert_k_bar('60Min')
    #         ck.convert_day_k_bar()
    #         last_close = ck.get_last_close()
    #         if last_close is not None:
    #             power_kbar(last_close)
    #         time.sleep(10)
    
    #開盤時間抓tick
    api.quote.subscribe(
        api.Contracts.Futures.TXF[globals.code],
        quote_type = sj.constant.QuoteType.Tick,
        version = sj.constant.QuoteVersion.v1,
    )
            
    @api.on_tick_fop_v1()

    def quote_callback(exchange:Exchange, tick:TickFOPv1):
        if tick.simtrade == True: return #避開試搓時間
        ck = convertK(tick,True)
        
        #最後一盤資料寫入csv
        current_time = datetime.datetime.now().time().replace(second=0, microsecond=0)
        if current_time == datetime.time(hour=4, minute=59) or current_time == datetime.time(hour=13, minute=44):
            globals.amount.append(tick.close)
            logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
            logging.debug('4:59 or 13:44')
            logging.debug(globals.amount)
            
        globals.now_min = ck.get_now_min()
        globals.tick_min = ck.get_tick_min()
        if globals.now_min == globals.tick_min: #現在的分鐘數與tick分鐘相符合就收集資料
            globals.volume += tick.volume
            if tick.close not in globals.amount: #排除重覆資料
                globals.amount.append(tick.close)
        else:
            ck.write_1k_bar(globals.tick_min,globals.volume,globals.amount)
            globals.now_min = None
            globals.amount.clear()
            globals.volume = tick.volume
            ck.convert_k_bar('5Min')
            ck.convert_k_bar('15Min')
            ck.convert_k_bar('30Min')
            print(tick.close)
            power_kbar(tick.close)
        
    threading.Event().wait()
    api.logout()

    #最後一盤資料寫入各分k
    current_time = datetime.datetime.now().time().replace(second=0, microsecond=0)
    if current_time == datetime.time(hour=5, minute=00) or current_time == datetime.time(hour=13, minute=45):
        logging.debug('5:00 or 13:45')
        df_tick = pd.read_csv('data/tick.csv', index_col='datetime')
        for index, row in df_tick.iterrows():
            globals.amount.append(row['close'])
            globals.volume += row['volume']      
            now = datetime.datetime.now()
            last_min  = now.strftime('%Y/%m/%d %H:%M')
            ck = convertK(row,True)
            ck.write_1k_bar(last_min,globals.volume,globals.amount)
            ck.convert_k_bar('5Min')
            ck.convert_k_bar('15Min')
            ck.convert_k_bar('30Min')