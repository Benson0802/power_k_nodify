def initialize(): 
    global now_min #即時的分鐘
    global tick_min #tick的分鐘
    global volume #這一分鐘tick的累積量
    global amount #這一分鐘收集的tick收盤價
    global code #台指期月份
    global min1_last
    global min5_last
    global min15_last
    global min30_last
    global line_token
    global has_order
    global op_h
    global op_l
    now_min = None
    tick_min = None
    volume = 0
    amount = []
    code = ''
    min1_last = None
    min5_last = None
    min15_last = None
    min30_last = None
    line_token = []
    has_order = False
    op_h = 0
    op_l = 0