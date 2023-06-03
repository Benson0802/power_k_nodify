def initialize(): 
    global now_min #即時的分鐘
    global tick_min #tick的分鐘
    global volume #這一分鐘tick的累積量
    global amount #這一分鐘收集的tick收盤價
    global code #台指期月份
    global line_token
    global has_order
    global min1_op_h
    global min1_op_l
    global min1_notify_time
    global min1_maturity_time
    global min5_op_h
    global min5_op_l
    global min5_notify_time
    global min5_maturity_time
    global min15_op_h
    global min15_op_l
    global min15_notify_time
    global min15_maturity_time
    global min30_op_h
    global min30_op_l
    global min30_notify_time
    global min30_maturity_time
    global min_buy
    now_min = None
    tick_min = None
    volume = 0
    amount = []
    code = ''
    line_token = []
    has_order = False
    min1_op_h = 0
    min1_op_l = 0
    min1_notify_time = None
    min1_maturity_time = None
    min5_op_h = 0
    min5_op_l = 0
    min5_notify_time = None
    min5_maturity_time = None
    min15_op_h = 0
    min15_op_l = 0
    min15_notify_time = None
    min15_maturity_time = None
    min30_op_h = 0
    min30_op_l = 0
    min30_notify_time = None
    min30_maturity_time = None
    min_buy = 0