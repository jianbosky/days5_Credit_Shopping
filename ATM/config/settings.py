#!/usr/bin/env python3.5
# -*-coding:utf8-*-
import datetime,pickle,os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# 加载利息计算日志文件
if os.path.exists(r'%s/config/calculation_log.txt'% BASE_DIR):
    f_calculation = open("%s/config/calculation_log.txt" % BASE_DIR, "rb")
    data_calculation = pickle.loads(f_calculation.read())
    # 利息初始化文件
    # print(data_calculation)
    f_calculation.close()
else:
    data_calculation = []
# 加载用户信息
if os.path.exists(r'%s/config/user_acc.txt'% BASE_DIR):
    f = open("%s/config/user_acc.txt" % BASE_DIR, "rb")
    data = pickle.loads(f.read())
    f.close()
else:
    data = []
# 加载消费明细
if os.path.exists(r'%s/config/user_list.txt'% BASE_DIR):
    f_list = open("%s/config/user_list.txt" % BASE_DIR, "rb")
    data_list = pickle.loads(f_list.read())
    f_list.close()
else:
    data_list = []
# 初始化利息计算文件列表
def calculation_computer():
    global data, data_calculation, data_list
    # 获取今天时间
    today = datetime.date.today()
    # 取昨天的时间
    yesterday = datetime.date.today()+datetime.timedelta(days=-1)
    for user_data in data:
        if user_data["flage"] == "2":
            # 获取 账单日
            x_data_date = user_data["Repayment_Date"]
            # 生成账单日期
            x_data_time = today.replace(day=x_data_date)
            # 如果文件内容不为空
            if len(data_calculation) != 0:
                for y_data in data_calculation:
                    # 如果信用卡卡号在文件字典里存在关键字
                    if user_data["usercard"] in y_data.keys():
                        for x in y_data[user_data["usercard"]]:
                            # 如果该字典里存在今天新加的记录则跳出
                            if x["date"] == today:
                                break
                            # 如果字典里的日期与昨天有误差则进行增加
                            elif yesterday > y_data[user_data["usercard"]][-1]["date"]:
                                date = y_data[user_data["usercard"]][-1]["date"] + datetime.timedelta(days=1)
                                y_data[user_data["usercard"]].append({"date":date,"money":0,"computer":"1"})
                                continue
                        else:
                            y_data[user_data["usercard"]].append({"date":today,"money":0,"computer":"1"})
                            break
                # 如果全部循环后找不到key 则新增
                else:
                    # 重复数据判断
                    list_data = []
                    for y_data in data_calculation:
                        for k in y_data:
                            list_data.append(k)
                    # 如果要添加的数据在利息初始化文件中不存大
                    if user_data["usercard"] not in list_data:
                        if today > x_data_time:
                            new_dic = {user_data["usercard"]:[{"date":x_data_time,"money":0,"computer":"1"}]}
                            data_calculation.append(new_dic)
                        elif today < x_data_time:
                            new_dic = {user_data["usercard"]:[{"date":today,"money":0,"computer":"1"}]}
                            data_calculation.append(new_dic)
                # 将所有利息数据写入文件中
                fl = open("%s/config/calculation_log.txt" % BASE_DIR, "wb")
                pickle.dump(data_calculation, fl)
                fl.close()
            # 如果文件内容为空
            else:
                # 时间按账单日开始记录
                if today > x_data_time:
                    new_dic = {user_data["usercard"]:[{"date":x_data_time,"money":0,"computer":"1"}]}
                    data_calculation.append(new_dic)
                elif today < x_data_time:
                    new_dic = {user_data["usercard"]:[{"date":today,"money":0,"computer":"1"}]}
                    data_calculation.append(new_dic)
                fl = open("%s/config/calculation_log.txt" % BASE_DIR, "wb")
                pickle.dump(data_calculation, fl)
                fl.close()
                calculation_computer()
# 出账单及利息计算
def computer():
    global data, data_calculation, data_list
    # 调用利息初始化文件
    calculation_computer()
    # 获取今天时间
    today = datetime.date.today()
    for x_data in data:
        if x_data["flage"] == "2":
            x_usercard = x_data["usercard"]   # 获取计算信用卡卡号
            # 获取账单还款到期日，每月10号
            due_date = today.replace(day=10)
            # 如果到期还款日小于账单日，当前利息计算日 ＝ 当月计算利息日－30天
            xx_time = due_date + datetime.timedelta(days=-30)
            # 加载消费明细账单
            for z_data in data_list:
                # 定位当前用户所有没有出账单的明细,如果今天大于或等于该笔消费出账单日
                if z_data["usercard"] == x_usercard and z_data["bills"] == "2" and today >= z_data["Statement_Date"]:
                    # 则更改当前该笔消费为已出账单
                    z_data["bills"] = "1"
            f_list_computer = open("%s/config/user_list.txt" % BASE_DIR, "wb")
            pickle.dump(data_list, f_list_computer)
            f_list_computer.close()
            # 调用利息计算初始化文件
            for xy_data in data_calculation:
                # 定位到当前用户下所有记账日
                if x_usercard in xy_data.keys():
                    for date in xy_data[x_usercard]:
                        if date["computer"] == "1":
                            # 定位到当前用户下所有出账单的未还清的消费记录
                            # 初始化记账日所有利息
                            counter = 0
                            for z1_data in data_list:
                                # 如果记账日没有清算
                                 if z1_data["usercard"] == x_usercard and z1_data["bills"] == "1":
                                    # 如果记账日大于最后还款日大于账单日
                                    if date["date"] > due_date > z1_data["Statement_Date"] and z1_data["state"] == "1":
                                        z1_data["interest"] += (z1_data["money"]+z1_data["Counter"])*0.0005
                                        counter += (z1_data["money"]+z1_data["Counter"])*0.0005
                                    # 如果记账日小于出账单日或小于最后还款日
                                    elif date["date"] > xx_time > z1_data["Statement_Date"] and z1_data["state"] == "1":
                                        z1_data["interest"] += (z1_data["money"]+z1_data["Counter"])*0.0005
                                        counter += (z1_data["money"]+z1_data["Counter"])*0.0005
                            x_data["new_money"] -= counter  # 更新当前用户的余额
                            f_list_computer = open("%s/config/user_list.txt" % BASE_DIR, "wb")
                            pickle.dump(data_list,f_list_computer)
                            f_list_computer.close()
                            date["computer"] = "2"
                            continue
                    break
            fl = open("%s/config/calculation_log.txt" % BASE_DIR, "wb")
            pickle.dump(data_calculation, fl)
            fl.close()
    fx = open("%s/config/user_acc.txt" % BASE_DIR, "wb")
    pickle.dump(data, fx)
    fx.close()
