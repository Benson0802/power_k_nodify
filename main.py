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

globals.initialize()
obj = check_opening()
year_mon = obj.get_year_mon()
globals.code = 'TXF' + str(year_mon['year']) + ('0' if len(str(year_mon['mon'])) == 1 else '') + str(year_mon['mon'])


def power_kbar():
    '''
     能量K棒計算
    '''
    df_1 = pd.read_csv('data/1Min.csv')
    df_1Min = df_1.iloc[-2]
    df_5 = pd.read_csv('data/5Min.csv')
    df_5Min = df_5.iloc[-2]
    df_15 = pd.read_csv('data/15Min.csv')
    df_15Min = df_15.iloc[-2]
    df_30 = pd.read_csv('data/30Min.csv')
    df_30Min = df_30.iloc[-2]

    if globals.min1_last == df_1Min['datetime']:
        return
    else:
        if df_1Min['volume'] >= 1000:
            get_power_data(1,df_1Min)
            globals.min1_last = df_1Min['datetime']
    
    if globals.min5_last == df_5Min['datetime']:
        return
    else:
        if df_5Min['volume'] >= 1000:
            get_power_data(5,df_5Min)
            globals.min5_last = df_5Min['datetime']
        
    if globals.min15_last == df_15Min['datetime']:
        return
    else:
        if df_15Min['volume'] >= 1000:
            get_power_data(15,df_15Min)
            globals.min15_last = df_15Min['datetime']
        
    if globals.min30_last == df_30Min['datetime']:
        return
    else:
        if df_30Min['volume'] >= 1000:
            get_power_data(30,df_30Min)
            globals.min30_last = df_30Min['datetime']

def get_power_data(minute,df):
    
    volume = float(str(df['volume'])[0] + '.' + str(df['volume'])[1:]) if int(
        str(df['volume'])[0]) < 6 else float('0.' + str(df['volume']))
    
    color = None
    datetime = df['datetime']
    power = math.ceil((df['high'] - df['low']) * volume)
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
    
    lineMsgFormat(minute,datetime,color,df['close'],df['volume'],power,hh,h,l,ll,op_h,op_l)

def lineMsgFormat(minute,datetime,color,close,volume,power,hh,h,l,ll,op_h,op_l):
    msg = "\n頻率："+str(minute)+'分鐘圖\n'
    msg += "時間日期："+str(datetime)+"\n"
    msg += "台股指數近月\n"
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
    sendMessage(msg)

def sendMessage(message):
    headers = { "Authorization": "Bearer " + globals.line_token }
    data = { 'message': message }
    requests.post("https://notify-api.line.me/api/notify",headers = headers, data = data)


with open('API_KEY.json', 'r') as f:
    json_data = json.load(f)
    globals.line_token = json_data['line_token']
    api = sj.Shioaji()
    api.login(
        api_key=json_data['api_key'],
        secret_key=json_data['secret_key'],
        contracts_cb=lambda security_type: print(f"{repr(security_type)} fetch done.")
    )

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
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
        logging.debug('4:59 or 13:44')
        ck.write_tick("tick")
        #最後一盤資料寫入各分k
        if current_time == datetime.time(hour=5, minute=0) or current_time == datetime.time(hour=13, minute=45):
            logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
            logging.debug('5:00 or 13:45')
            df_tick = pd.read_csv('data/tick.csv', index_col='datetime')
            for index, row in df_tick.iterrows():
                globals.amount.append(row['close'])
                globals.volume += row['volume']
                        
            now = datetime.datetime.now()
            last_min  = now.strftime('%Y/%m/%d %H:%M')
            ck = convertK(tick,True)
            ck.write_1k_bar(last_min,globals.volume,globals.amount)
            ck.convert_k_bar('5Min')
            ck.convert_k_bar('15Min')
            ck.convert_k_bar('30Min')
            # ck.convert_k_bar('60Min')
            # ck.convert_day_k_bar()
    
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
        # ck.convert_k_bar('60Min')
        # ck.convert_day_k_bar()
        power_kbar()

threading.Event().wait()
api.logout()
