import numpy as pt
import datetime


class Tool():
    #默认设置无风险利率为3%
    Risk_free_rate = 3
    def __init__(self,data_list):
        self.data_dict = data_list
    #slef.date_dict是一个关于 时间(date 类型为str) 涨跌（change 类型为float ） 净值(networth 类型为float)
    #通过调用self.data_dict计算出最大回撤
    def calculate_max_drawdown(self):
        net = []
        drawlist = []
        for i in self.data_dict:
            net.append(i['net_worth'])
        for i in net:
            ind = net.index(i)
            for j in net[ind:]:
                drawdown = (i - j) / i
                drawlist.append(drawdown)
        drawdown_fin = max(drawlist)
        dra = round(drawdown_fin * 100, 2)
        return str(dra) + "%"

    #通过调用self.data_dict计算出年化波动率
    def calculate_annualized_volatility(self):
        cha = []
        for i in self.data_dict:
            cha.append(i['change'])
        cha_std = pt.std(cha)
        annualized_volatility = cha_std * ((250) ** 0.5)
        ann = round(annualized_volatility, 2)
        # print(ann)
        return ann

   #    #通过调用self.data_dict计算出夏普比
    def calculate_sharpe_ratio(self):
        annualized_yield = self.calculate_annualized_yield()
        annualized_volatility = self.calculate_annualized_volatility()
        sharpe_ratio = (annualized_yield-self.Risk_free_rate)/annualized_volatility
        sha = round(sharpe_ratio, 2)
        # print(sha)
        return sha

    #通过调用self.data_dict计算出年化收益率
    def calculate_annualized_yield(self):
        cha = []
        for i in self.data_dict:
            cha.append(i['net_worth'])
        date_li = []
        for i in self.data_dict:
            date_li.append(i['date'])
        # 计算日期差
        first_date_y = int(date_li[0][0:4])
        first_date_m = int(date_li[0][5:7])
        first_date_d = int(date_li[0][8:10])
        last_date_y = int(date_li[len(date_li) - 1][0:4])
        last_date_m = int(date_li[len(date_li) - 1][5:7])
        last_date_d = int(date_li[len(date_li) - 1][8:10])
        first_date = datetime.datetime(first_date_y, first_date_m, first_date_d)
        last_date = datetime.datetime(last_date_y, last_date_m, last_date_d)
        day = last_date - first_date
        diff_wor = (cha[len(cha)-1] - cha[0]) / cha[0]
        annualized_yield = diff_wor / abs(day.days) * 365
        ann_u = round(annualized_yield*100, 2)
        # print(ann_u)
        return ann_u

