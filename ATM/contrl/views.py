#!/usr/bin/env python3.5
# -*-coding:utf8-*-
import os,pickle,sys,datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from contrl.management import User_Action
#加载ATM用户数据库
if os.path.exists(r'%s/config/user_acc.txt'% BASE_DIR):
    f = open("%s/config/user_acc.txt" % BASE_DIR, "rb")
    data_user = pickle.loads(f.read())
    f.close()
# 加载ATM操作日志信息
if os.path.exists(r'%s/config/user_log.txt'% BASE_DIR):
    fl = open("%s/config/user_log.txt" % BASE_DIR, "rb")
    data_log = pickle.loads(fl.read())
    fl.close()

# 消费明细
if os.path.exists(r'%s/config/user_list.txt'% BASE_DIR):
    f_list = open("%s/config/user_list.txt" % BASE_DIR, "rb")
    data_list = pickle.loads(f_list.read())
    f_list.close()
else:
    data_list = []

# 消费明细增加
def sale_add(usercard,usermoney_input,action,state,bills,remarks,Counter=0,interest=0):
    global data_user
    today =datetime.date.today()
    for x_data in data_user:
        if x_data["usercard"] == usercard:
            date = x_data["Repayment_Date"]
            # 计算账单日
            Statement_Date = today.replace(day=date)
            if today > Statement_Date:
                Statement_Date = Statement_Date + datetime.timedelta(days=+30)  # 如果今天消费的日期 大于系统计算出来的账单日，则此笔消费的出账单为下个月
    data_list_dic = {}
    data_list_dic["usercard"] = usercard
    data_list_dic["date"] = datetime.datetime.now()
    data_list_dic["money"] = usermoney_input
    data_list_dic["action"] = action  # 1、信用卡取现 2、转账 3、消费 4、还款
    data_list_dic["state"] = state   # 1、已欠款 2、已还清
    data_list_dic["bills"] = bills   # 1、已出账单 2、未出账单
    data_list_dic["Counter"] = Counter  # 手续费
    data_list_dic["interest"] = interest  # 利息
    data_list_dic["Statement_Date"] = Statement_Date  # 出账单日
    data_list_dic["remarks"] = remarks
    data_list.append(data_list_dic)
    f_list = open("%s/config/user_list.txt" % BASE_DIR, "wb")
    pickle.dump(data_list,f_list)
    f_list.close()

# 查询余额函数
def select_balance(usercard,flage):
    # 定义全局变量
    global data_user
    if flage =="2":
        for x_name in data_user:
            # 匹配用户信息
            if x_name["usercard"] == usercard:
                if x_name["new_money"] - x_name["total_money"] >=0:
                    print("""
                您当前可用余额为:%s元,当前信用卡授权额度为%s元，出账单日为每月%s号,当前没有欠款，谢谢！
                """%(x_name["new_money"],x_name["total_money"],x_name["Repayment_Date"]))
                else:
                    print("""
                    您当前可用余额为:%s元,当前信用卡授权额度为%s元，出账单日为每月%s号，当前总欠款%s元，请按时还款！
                    """%(x_name["new_money"],x_name["total_money"],x_name["Repayment_Date"],(x_name["total_money"]-x_name["new_money"]) ))

    else:
        print("请求参数出错，请检查后在试！")
# 查询ATM操作日志
def select_log():
    print("ATM操作日志：")
    for index,x_log in enumerate(data_log):
        x_date = x_log["cz_time"]
        cz_user = x_log["cz_usercard"]
        x_action = x_log["cz_action"]
        x_money = x_log["cz_money"]
        x_user = x_log["cz_adduser"]
        print("-" *200)
        print("序号:[%s]|操作日期:[%s]|操作用户:[%s]｜动作:[%s]|涉及金额:%s元|对象用户:[%s]" %(index+1,x_date,cz_user,x_action,x_money,x_user))

# ATM 取现：
def Take_Money(usercard,usermoney_input,flage):
    global data_user,data_list
    for x_name in data_user:
        if x_name["usercard"] == usercard:
            # 判断可用额度是否满足取现的金额
            if x_name["new_money"] - usermoney_input >= 0:
                Counter = usermoney_input*0.05   # 取现手续费
                x_name["new_money"] -= (usermoney_input + Counter)
                # 写日志
                User_Action(usercard,flage,usercard,"信用卡取款",usermoney_input)
                # 写消费明细
                if x_name["new_money"] >= x_name["total_money"]:
                    sale_add(usercard,usermoney_input,"1","2","2","取现",Counter)
                else:
                    sale_add(usercard,usermoney_input,"1","1","2","取现",Counter)
                print("取现[%s],成功！"%(usermoney_input))
            else:
                print("您当前取现额度超过你信用卡的可用额度，不能取现！")
    f = open("%s/config/user_acc.txt" % BASE_DIR, "wb")
    pickle.dump(data_user, f)
    f.close()

# 信用卡还款
def Card_Payment(usercard,money,flage="3"):
    global data_user,data_list
    for x_name in data_user:
        if x_name["usercard"] == usercard:
            x_name["new_money"] += money
            if flage != "3":
                print("还款入账成功")
            sale_add(usercard,money,"4","2","2","还款入账")
            # 提前全额还款处理
            if x_name["new_money"] >= x_name["total_money"]:
                for list_name in data_list:
                    if list_name ["usercard"] == usercard:
                        if list_name ["state"] != "2":
                            list_name ["state"] = "2"
                f_list = open("%s/config/user_list.txt" % BASE_DIR, "wb")
                pickle.dump(data_list,f_list)
                f_list.close()
            # 提前部分还款处理
            else:
                for list_name in data_list:
                    if list_name ["usercard"] == usercard:
                        if list_name ["state"] != "2":
                            if list_name["money"] < money:
                                money -= list_name["money"]
                                list_name["state"] = "2"
                f_list = open("%s/config/user_list.txt" % BASE_DIR, "wb")
                pickle.dump(data_list,f_list)
                f_list.close()
    # 写还款日志
    User_Action(usercard,flage,usercard,"信用卡还款",money)
    f = open("%s/config/user_acc.txt" % BASE_DIR, "wb")
    pickle.dump(data_user, f)
    f.close()
# 账户转账
def Transfer(usercard,flage,usercard_input,usermoney_input):
    global data_user
    for input_name in data_user:
        if input_name["usercard"] == usercard:
            input_name["new_money"] -= usermoney_input
            # 写消费明细
            if input_name["new_money"] >= input_name["total_money"]:
                sale_add(usercard,usermoney_input,"2","2","2","转账")
            else:
                sale_add(usercard,usermoney_input,"2","1","2","转账")
            # 写日志
            User_Action(usercard,flage,usercard_input,"信用卡转账",usermoney_input)
            # 调用转账还款入账函数
            Card_Payment(usercard_input,usermoney_input)
            print("转账成功！")
    f = open("%s/config/user_acc.txt" % BASE_DIR, "wb")
    pickle.dump(data_user, f)
    f.close()
# 账单明细查询
def select_bill(usercard,bill_date):
    global data_list
    # 已出账单明细
    have_bill = []
    # 未出账单明细
    No_bills = []
    # 未出账单还款入账
    repayment = []
    # 未出账单已还清
    Already = []
    for index,x_name in enumerate(data_list):
        if x_name["usercard"] == usercard:
            # 欠款未出账单消费明细
            if x_name["state"] == "1" and x_name["bills"] == "2":
                No_bills.append(data_list[index])
            # 欠款已出账单消费明细
            elif x_name["state"] == "1" and x_name["bills"] == "1":
                have_bill.append(data_list[index])
            # 转账还款入账明细
            elif x_name["bills"] == "2" and x_name["action"] == "4":
                repayment.append(data_list[index])
            # 已还清未出账单明细
            elif x_name["bills"] == "2" and x_name["state"] == "2":
                Already.append(data_list[index])

    if len(have_bill) != 0:
        print("以下消费为已出账单未还清明细：")
        for index,have_bill_list in enumerate(have_bill):
            x_date = have_bill_list["date"]
            x_action = have_bill_list["remarks"]
            x_money = have_bill_list["money"]
            x_Counter = have_bill_list["Counter"]
            x_Statement_Date = have_bill_list["Statement_Date"]
            x_state = "未还清"
            x_interest = have_bill_list["interest"]
            print("-" *150)
            print("序号:[%s]|日期:[%s]|类型:[%s]｜金额:[%s]元|手续费:%s元|状态:[%s]|此笔交易出账单日[%s]|累计利息为:%s元" %(index+1,x_date,x_action,x_money,x_Counter,x_state,x_Statement_Date,x_interest))
    if len(No_bills) != 0:
        print("以下消费为未出账单未还清明细：")
        for index,No_bills_list in enumerate(No_bills):
            x_date = No_bills_list["date"]
            x_action = No_bills_list["remarks"]
            x_money = No_bills_list["money"]
            x_Counter =No_bills_list["Counter"]
            x_Statement_Date = No_bills_list["Statement_Date"]
            x_state = "未还清"
            print("-" *100)
            print("序号:[%s]|日期:[%s]|类型:[%s]｜金额:[%s]元|手续费:%s元|状态:[%s]|此笔交易出账单日[%s]" %(index+1,x_date,x_action,x_money,x_Counter,x_state,x_Statement_Date))
    if len(repayment) != 0:
        print("以下为未出账单还款明细：")
        for index,repayment_list in enumerate(repayment):
            x_date = repayment_list["date"]
            x_action = repayment_list["remarks"]
            x_money = repayment_list["money"]
            x_Counter = repayment_list["Counter"]
            x_state = "还款入账"
            print("-" *100)
            print("序号:[%s]|日期:[%s]|类型:[%s]｜金额:[%s]元|手续费:%s元|状态:[%s]" %(index+1,x_date,x_action,x_money,x_Counter,x_state))
    if len(Already) != 0:
        print("以下为未出账单已还款或无需还款消费明细：")
        for index,Already_repayment_list in enumerate(Already):
            x_date = Already_repayment_list["date"]
            x_action = Already_repayment_list["remarks"]
            x_money = Already_repayment_list["money"]
            x_Counter = Already_repayment_list["Counter"]
            x_state = "正常"
            print("-" *100)
            print("序号:[%s]|日期:[%s]|类型:[%s]｜金额:[%s]元|手续费:%s元|状态:[%s]" %(index+1,x_date,x_action,x_money,x_Counter,x_state))


