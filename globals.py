def initialize(): 
    global now_min #即時的分鐘
    global tick_min #tick的分鐘
    global volume #這一分鐘tick的累積量
    global amount #這一分鐘收集的tick收盤價
    global code #台指期月份
    global line_token
    global today
    global day_color
    now_min = None
    tick_min = None
    volume = 0
    amount = []
    code = ''
    line_token = []
    today = None
    day_color = None