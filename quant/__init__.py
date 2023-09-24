# @Version: python3.10
# @Time: 2023/9/24 8:48
# @Author: PlutoCtx
# @Email: 15905898514@163.com
# @File: __init__.py.py
# @Software: PyCharm
# @User: chent

# timedelta用来计算时间 用来推算过去未来的时间
from datetime import timedelta, datetime

import numpy as np
import pandas as pd
from keras.layers import LSTM, Dense
from keras.models import Sequential
from sklearn.externals import joblib


# 初始化账户
def init(context):
    # 设置基准收益：中证800指数
    set_benchmark('000906.SH')
    # 打印日志
    log.info('策略开始运行')
    # 训练集x的天数
    context.num_x_days = 7
    # 训练集y的天数
    context.num_y_days = 7
    # 训练集y的涨幅
    context.index_rise = 0.02
    # 调仓周期
    context.cycle = 1
    # 止盈参数
    context.index_profit = 0.06
    # 止损参数
    context.index_loss = -0.06
    # 持仓数量
    context.num_hold_stocks = 500

    # 调仓信号
    context.cycle_flag = True
    # 下一个调仓的日期
    context.transfer_positions_date = get_next_date(get_datetime(), context.cycle_flag)

    get_iwencai('所有A股', 'stocks_list')
    # 早期训练集和测试集的获取，以及模型训练产生文件
    #     train_date_st=datetime(2012, 1, 1)
    #     train_date_length = 60
    #     train_date_step = 30
    #     X_array, label = create_train_data(train_date_st, context)

    #     for i in range(1, train_date_length):
    #         now_date = train_date_st + timedelta(i * train_date_step)
    #         unit_X_array, unit_label = create_train_data(now_date, context)
    #         X_array = np.concatenate((X_array, unit_X_array), axis=0)
    #         label += unit_label

    #     train_size = 60 * train_date_length
    #     context.scaler = preprocessing.StandardScaler().fit(X_array)

    # #最后一列的数据
    #     X_train = X_array[:-train_size]
    # #行号为最后一行的数据
    #     X_test = X_array[-train_size:]
    #     Y_train = label[:-train_size]
    #     Y_test = label[-train_size:]
    #     model = optimize_LSTM(X_train, X_test, Y_train, Y_test)

    #     context.scaler = preprocessing.StandardScaler().fit(X_array)
    #     df_scaler = context.scaler.transform(X_array)
    #     context.clf = svm.SVC(C=30.15, gamma=0.001100009)
    #     context.clf.fit(df_scaler, np.array(label))
    #     joblib.dump(context.clf, 'CLF1.joblib')
    #     joblib.dump(context.scaler, 'clf_scaler.joblib')

    context.scaler = joblib.load('clf_scaler.joblib')
    context.clf = joblib.load('CLF1.joblib')

    # 设置股票每笔交易的手续费为万分之二(手续费在买卖成交后扣除,不包括税费,税费在卖出成交后扣除)
    set_commission(PerShare(type='stock', cost=0.0001))
    # 设置股票交易滑点0.5%,表示买入价为实际价格乘1.005,卖出价为实际价格乘0.995
    set_slippage(PriceSlippage(0.005))
    # 设置日级最大成交比例25%,分钟级最大成交比例50%
    # 日频运行时，下单数量超过当天真实成交量25%,则全部不成交
    # 分钟频运行时，下单数量超过当前分钟真实成交量50%,则全部不成交
    set_volume_limit(0.25, 0.5)

    # 设定持仓数量
    g.stock_num = 10
    # 以深圳中小盘指数 均线进行择时参考
    g.MA_reference = ['399101.SZ', 10]
    # 牛熊判断相关参数
    g.isbull = False  # 是否牛市
    g.threshold = 0.003  # 牛熊切换阈值
    g.choose_time_signal = False  # 启用择时信号

    # 熊市仓位比例
    g.PositionPercentageWhenIsBear = 0.8  # 熊市3成仓位 数值是0到1之间 [0,1]

    # 回测区间、初始资金、运行频率
    # 每周运行
    # 每周第一个交易日执行
    run_weekly(func=Trade, date_rule=1, reference_security='000001.SZ')


# 设定熊市仓位比例系数，把实际购买金额按照系数进行打折
def get_bull_bear_discount_num():
    if g.isbull:
        return 1
    else:
        return g.PositionPercentageWhenIsBear


# 设置牛熊全局变量 方便 仓位控制时候调用
def setting_bull_bear_signal(context):
    # 运行牛熊判断函数, 返回g.isbull
    temp0 = g.isbull
    get_bull_bear_signal_minute()
    temp1 = g.isbull
    if temp0 and not temp1:
        g.direction = -1  # 牛转熊: -1;
    elif not temp0 and temp1:
        g.direction = 1  # 熊转牛 +1;
    else:
        g.direction = 0  # 牛熊不变: 0;
    if g.isbull:
        log.info("当前市场判断为：牛市")
    else:
        log.info("当前市场判断为：熊市")


# 牛熊市场判断函数
def get_bull_bear_signal_minute():
    # 获取时间
    day_last = get_datetime() - datetime.timedelta(days=1)
    yesterday_date = day_last.strftime("%Y%m%d")
    # stock_list_399101 = get_index_stocks(g.MA[0],yesterday_date)

    # 获取399101.XS的MA10
    closes = \
        get_price(g.MA_reference[0], None, yesterday_date, '1d', ['close'], True, None, bar_count=g.MA_reference[1],
                  is_panel=1)['close']
    now_index = closes[-1]
    MAold = closes.mean()
    if g.isbull:
        # 现价比10日均价低，两者差值大于阈值时转熊
        if now_index * (1 + g.threshold) <= MAold:
            g.isbull = False
    else:
        # 现价比10日均价高，两者差值大于阈值时转牛
        if now_index > MAold * (1 + g.threshold):
            g.isbull = True


# 过滤科创_北交所_三板
def filter_bjkc_stock(stock_list):
    for i in range(len(stock_list) - 1, -1, -1):
        if stock_list[i][0] == '8' or stock_list[i][:2] == '68' or stock_list[i][0] == '4':
            stock_list.pop(i)
    return stock_list


def Trade(context, bar_dict):
    day_last = get_datetime() - datetime.timedelta(days=1)  # 获取计算市值的日期
    yesterday_date = day_last.strftime("%Y%m%d")
    log.info(yesterday_date)
    all_stock = filter_st()  # 过滤ST
    all_stock = filter_bjkc_stock(all_stock)  # 过滤科创、北交
    # 获取市值数据，并按照市值升序输出
    choice = get_fundamentals(query(
        valuation.symbol,
        valuation.market_cap
    ).order_by(
        valuation.market_cap.asc()).filter(valuation.symbol.in_(all_stock)).limit(g.stock_num))[
        'valuation_symbol'].tolist()
    # 如果上月持仓的股票不在当月股票池中，进行平仓
    for s in context.portfolio.positions:
        if (s not in choice):
            order_target(s, 0)

    # 刷新牛熊全局变量
    setting_bull_bear_signal(context)
    # 获取当前的仓位打折系数。
    bear_disCount = get_bull_bear_discount_num()

    # 等权买入
    psize = 1.0 / g.stock_num * context.portfolio.total_value * bear_disCount
    for s in choice:
        if context.portfolio.available_cash < psize:
            break
        if s not in context.portfolio.positions:
            order_value(s, psize)


# 每日开盘前 9:00 被调用一次, 用于储存自定义参数、全局变量, 执行盘前选股等
def before_trading(context):
    # 获取日期
    date = get_datetime().strftime('%Y-%m-%d %H:%M:%S')
    # 打印日期
    log.info('{} 盘前运行'.format(date))


# 设置买卖条件，每个交易频率(日/分钟/tick)调用一次
def handle_bar(context, bar_dict):
    # 获取时间
    time = get_datetime().strftime('%Y-%m-%d %H:%M:%S')
    # 打印时间
    log.info('当天时间' + str(time))
    # 获取当天数据，取得预测结果

    date = get_datetime()
    # today_date = TransTime(date)
    today_date = date.strftime("%Y%m%d")
    # 账户信息里面的仓位信息 获取仓库的数量
    # 账户财产信息列表的长度
    num_stocks = len(list(context.portfolio.positions))
    #     context.cycle_flag 表示一个布尔变量，用于判断是否需要进行周期性的调仓。
    # today_date == context.transfer_positions_date 表示当前日期是否等于下一个调仓日期。
    # num_stocks < 5 表示仓位数量是否小于 5。
    if context.cycle_flag or today_date == context.transfer_positions_date or num_stocks < 5:
        print("-----------------进行调仓-------------------")
        context.cycle_flag = False
        context.transfer_positions_date = get_next_date(get_datetime(), context.cycle)
        print("下一个调仓的的日期" + str(context.transfer_positions_date))
        Transaction(context, bar_dict, date)

    saveProfit(context, bar_dict, context.securities, context.predicts, context.index_profit, context.index_loss)


def Transaction(context, bar_dict, date):
    context.group_num = 1
    # 因子分组
    context.number = 1
    # 资金分配
    context.clean_ty = "median_extremum-standardize"
    # 系统因子排序
    context.sys_sort = []
    # 因子比率
    context.sys_factors = {
        'equity_ratio': 0.1,
        'weighted_roe': 0.1,
        'parent_company_share_holders_net_profit_growth_ratio': 0.1,
        'pe': -0.1,
        'turnover_ratio_of_receivable': 0.1,
        'bias': -0.1,
        'macd': 0.1,
        'obv': 0.1,
        'arbr': 0.1,
        'boll': 0.1
    }
    # 用户因子筛选条件
    context.user_query = ""
    # 用户因子排序
    context.user_sort = []
    # 用户因子比率
    context.user_factors = {}
    # 筛选的股票
    context.securities = []
    nowtime_str = get_last_datetime().strftime("%Y-%m-%d")
    # 获取因子数据
    securities_df = sfactor_stock_scanner(
        context.stocks_list,
        query(factor.symbol,
              factor.equity_ratio,
              factor.weighted_roe,
              factor.parent_company_share_holders_net_profit_growth_ratio,
              factor.pe,
              factor.turnover_ratio_of_receivable,
              factor.bias,
              factor.macd,
              factor.obv,
              factor.arbr,
              factor.boll
              ),
        context.sys_sort,
        context.sys_factors,
        context.user_query,
        context.user_sort,
        context.user_factors,
        nowtime_str,
        context.clean_ty,
    )
    if len(securities_df):
        index_s, index_e = length_split(len(securities_df), context.group_num, context.number)
        context.securities.extend(list(securities_df.iloc[index_s:index_e]['symbol']))

    # context.securities = context.securities[:800]
    # print(context.securities)
    X_array = get_needed_X_array(date, context.securities, context.num_x_days)
    context.predicts = context.clf.predict(context.scaler.transform(X_array))
    for i in range(len(context.securities)):
        # 如果预测结果为1且未持仓，则买入
        if context.predicts[i] == 1 and context.securities[i] not in context.portfolio.positions.keys():
            # log.info('buying %s' %context.stocks[i])
            # order_percent(context.securities[i], 1 / context.num_hold_stocks)
            pass
        # # 如果预测结果为-1且已持仓，则清仓
        elif context.predicts[i] == -1 and context.securities[i] in context.portfolio.positions.keys():
            # log.info('selling %s' % context.stocks[i])
            # order_target(context.securities[i], 0)
            pass


def get_needed_X_array(current_date, stocks, num_x_days):
    # strftime("%Y%m%d")
    # time_start = TransTime(current_date-timedelta(days=num_x_days))
    time_start = (current_date - timedelta(days=num_x_days)).strftime("%Y%m%d")
    # time_end = TransTime(current_date)
    time_end = current_date.strftime("%Y%m%d")
    prices = get_price(stocks, start_date=time_start, end_date=time_end,
                       fields=['open', 'high', 'low', 'close', 'avg_price', 'amp_rate'])
    X_array = []
    for i in range(len(stocks)):
        # 均价
        meanPrice = np.mean(prices[stocks[i]]['avg_price'])
        # 收盘价
        finalPrice = prices[stocks[i]]['close'][-1]
        # 最大值
        maxPrice = max(prices[stocks[i]]['high'])
        # 最小值
        minPrice = min(prices[stocks[i]]['low'])
        # 现价
        nowPrice = prices[stocks[i]]['open'][-1]
        # 涨跌幅
        quoteRate = (prices[stocks[i]]['open'][-1] / prices[stocks[i]]['open'][0]) - 1
        # 标准差
        stdnow = np.std(prices[stocks[i]]['open'])
        # 组织成向量
        X = np.array([
            finalPrice / meanPrice,
            maxPrice / meanPrice,
            minPrice / meanPrice,
            nowPrice / meanPrice,
            quoteRate,
            stdnow,
            nowPrice
        ])
        X_array.append(X)
    X_array = np.array(X_array)
    # 返回当天的所有股票
    return X_array


def get_needed_label(select_data, stock, num_y_days):
    nowDate = select_data
    futureDate = select_data + timedelta(days=num_y_days)

    label = []
    # 格式化时间串
    idate = nowDate.strftime("%Y-%m-%d")
    fdate = futureDate.strftime("%Y-%m-%d")
    prices = get_price(stock, start_date=idate, end_date=fdate, fields=['open'])
    for i in range(len(stock)):
        if ((prices[stock[i]]['open'][1] / prices[stock[i]]['open'][0]) - 1 > 0.0140865):
            label.append(1)
        else:
            label.append(-1)

    return label


# datetime转换格式
def TransTime(date):
    return date.strftime("%Y%m%d")


# 获取训练数据
def create_train_data(select_data, context):
    stock = get_index_stocks(symbol='000906.SH', date=select_data.strftime("%Y-%m-%d"))
    X_array = get_needed_X_array(select_data, stock, context.num_x_days)
    label = get_needed_label(select_data, stock, context.num_y_days)
    return X_array, label


def optimize_LSTM(X_train, X_test, Y_train, Y_test):
    # 将输入数据转换为LSTM所需的3D张量形式：[样本数，时间步长，特征维度]
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    model = Sequential()
    model.add(LSTM(units=128, input_shape=(X_train.shape[1], 1)))
    model.add(Dense(units=1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train, Y_train, epochs=10, batch_size=32)

    score = model.evaluate(X_test, Y_test, verbose=0)
    print(score[1])  # 输出模型在测试集上的准确率
    return model


# 设置止损条件
def saveProfit(context, bar_dict, stock, predicts, index_profit, index_loss):
    print("根据盈亏线进行止盈止损")
    last_date = get_datetime()
    for i in range(len(stock)):
        # 如果stock里面信息在用户账户资产信息里面
        if stock[i] in context.portfolio.positions.keys():
            # print(stock[i])
            if context.portfolio.positions[stock[i]].available_amount > 0:
                purchase_price = context.portfolio.positions[stock[i]].cost_basis
                dic_close = get_last_minute_close_price([stock[i]], last_date)
                last_close3 = float(dic_close[stock[i]]['close'][-1])
                # last_close = bar_dict[stock[i]].close
                if (purchase_price != 0):
                    rate = (last_close3 - purchase_price) / purchase_price
                else:
                    rate = 0
                print("股票" + str(stock[i]) + "：")
                print("购买价格为" + str(purchase_price))
                print("上一分钟收盘价：" + str(last_close3))
                print("收益率：" + str(rate))

                if rate > index_profit:
                    # log.info('()执行止损'.format(last_date))
                    # log.info('卖出股票{}'.format(stock[i]))
                    X_array = get_needed_X_array(last_date, context.securities, context.num_x_days)
                    context.predicts = context.clf.predict(context.scaler.transform(X_array))
                    if context.predicts[i] == -1:
                        # order_target_value(stock[i], 0)
                        pass

                if rate < index_loss:
                    # log.info('()执行止盈'.format(last_date))
                    # log.info('卖出股票{}'.format(stock[i]))
                    try:
                        # order_target_value(stock[i], 0)
                        pass
                    except:
                        print("售出失败")


def get_last_minute_close_price(symbol_list, current_date):
    nowTime = current_date + timedelta(minutes=-1)
    nowTime = nowTime.strftime('%Y%m%d %H:%M')
    close_price_dict = get_price(symbol_list, None, nowTime, '1m', ['close'], True, None, 30, is_panel=0)
    return close_price_dict


# 跳过周末，获取想要的下一个交易日。输入为datetime格式
def get_next_date(date, days):
    date = date.strftime("%Y%m%d")

    # 获取时间的时间戳 时间戳表示从1970年1月1日开始按秒计算得到的偏移量 normalize表示将其格式化成午夜值
    date = pd.Timestamp(date).normalize()
    # 显示所有的交易日
    date_in = get_all_trade_days()
    # 用于在排序的数组arr中查找索引
    trade_date = date_in[date_in.searchsorted(date, side='left') + days]
    trade_date = trade_date.strftime("%Y%m%d")
    return trade_date


def length_split(length, group_num, number):
    if length == 0 or group_num == 0:
        return 0, 0
    return (number - 1) * int(length / group_num), number * int(length / group_num) if number != group_num else length


##过滤ST股-无未来函数
def filter_st():
    # 昨日所有股票列表
    day_last = get_datetime() - datetime.timedelta(days=1)
    yesterday_date = day_last.strftime("%Y%m%d")
    stock_list = list(get_all_securities('stock', yesterday_date).index)

    name_info = run_query(
        query(
            name_change.symbol,
            name_change.change_date,
            name_change.report_date,
            name_change.stock_name
        ).filter(
            name_change.change_date <= get_datetime().strftime('%Y-%m-%d')
        ).order_by(
            name_change.change_date
        )
    )
    name_info['name_change_stock_name'] = name_info['name_change_stock_name'].apply(
        lambda x: 'ST' in str(x) or '退' in str(x))
    name_info = name_info.groupby('name_change_symbol').last()
    st_list = list(name_info.loc[name_info['name_change_stock_name']].index)

    # print(st_list)
    # print(stock_list)

    return [s for s in stock_list if s not in st_list]


# 收盘后运行函数, 用于储存自定义参数、全局变量, 执行盘后选股等
def after_trading(context):
    # 获取时间
    time = get_datetime().strftime('%Y-%m-%d %H:%M:%S')
    # 打印时间
    log.info('{} 盘后运行'.format(time))
    log.info('一天结束')
