#!/usr/bin/env python3.5
# -*-coding:utf8-*-
import os,pickle,sys,datetime
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
if os.path.exists(r'%s/config/user_acc.txt'% BASE_DIR):
    f = open("%s/config/user_acc.txt" % BASE_DIR, "rb")
    data_user = pickle.loads(f.read())
    f.close()
# 加载ATM操作日志信息
if os.path.exists(r'%s/config/user_log.txt'% BASE_DIR):
    fl = open("%s/config/user_log.txt" % BASE_DIR, "rb")
    data_log = pickle.loads(fl.read())
    fl.close()
else:
    data_log = []

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
# ATM 操作日志增加函数
def User_Action(cz_usercard,cz_flage,usercard,user_action,money=0):
    global data_log
    data_log_add = {}
    data_log_add["cz_usercard"] = cz_usercard
    data_log_add["cz_flage"] = cz_flage
    data_log_add["cz_action"] = user_action
    data_log_add["cz_adduser"] = usercard
    data_log_add["cz_time"] = datetime.datetime.now()
    data_log_add["cz_money"] = money
    data_log.append(data_log_add)
    fl = open("%s/config/user_log.txt" % BASE_DIR, "wb")
    pickle.dump(data_log, fl)
    fl.close()
# 用户支付接口
def User_Pay_Api(input_usercard,input_password,money,flage ="2"):
    global data_user
    for user_data in data_user:
        if user_data["usercard"] == input_usercard and user_data["password"] == input_password:
            # 判断该信用卡是否被冻结
            if user_data["state"] == "on":
                if user_data["new_money"] - money >= 0:
                    user_data["new_money"] -= (money)
                    # 写ATM日志
                    User_Action(input_usercard,flage,input_usercard,"网上消费支出",money)
                    # 是否已欠款
                    if user_data["new_money"] - user_data["total_money"] >= 0:
                        sale_add(input_usercard,money,"3","2","2","网上消费支出")
                    else:
                        sale_add(input_usercard,money,"3","1","2","网上消费支出")
                    print("支付成功！")
                    break
                else:
                    print("余额不足！")
                    return 2
            else:
                print("该信用卡已被冻结！")
                return 3

    else:
        print("登陆失败（账号或密码错误）！")
        return 4
    f = open("%s/config/user_acc.txt" % BASE_DIR, "wb")
    pickle.dump(data_user, f)
    f.close()