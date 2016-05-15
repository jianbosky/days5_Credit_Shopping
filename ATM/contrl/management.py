#!/usr/bin/env python3.5
# -*-coding:utf8-*-
import pickle,os,datetime,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# 加载用户信息
if os.path.exists(r'%s/config/user_acc.txt'% BASE_DIR):
    f = open("%s/config/user_acc.txt" % BASE_DIR, "rb")
    data = pickle.loads(f.read())
    f.close()
else:
    data = []
# 加载ATM操作日志信息
if os.path.exists(r'%s/config/user_log.txt'% BASE_DIR):
    fl = open("%s/config/user_log.txt" % BASE_DIR, "rb")
    data_log = pickle.loads(fl.read())
    fl.close()
else:
    data_log = []
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
# 增加用户
def User_Add(cz_usercard,cz_flage,usercard,password,total_money,Repayment_Date,flage):
    global data
    data_list = []
    for user_data in data:
       data_list.append(user_data["usercard"])
    if usercard not in data_list:
        # 增加用户
        user_dic ={}
        user_dic["usercard"] = usercard
        user_dic["password"] = password
        user_dic["new_money"] = total_money
        user_dic["total_money"] = total_money
        user_dic["Repayment_Date"] = Repayment_Date
        user_dic["flage"] = flage
        user_dic["state"] = "on"
        data.append(user_dic)
        f = open("%s/config/user_acc.txt" % BASE_DIR, "wb")
        pickle.dump(data, f)
        f.close()
        User_Action(cz_usercard,cz_flage,usercard,"增加用户")
        print("增加卡号[%s],成功！"%(usercard))
    else:
        print("增加信用卡卡号失败，原因：[“已存在”]")
# 解冻信用卡
def User_thaw(usercard,cz_usercard,cz_flage):
    global data
    # 判断是否为管理员账号
    if cz_flage =="1":
        for x_name in data:
            if x_name["usercard"] == usercard:
                x_name["state"] = "on"
        f = open("%s/config/user_acc.txt" % BASE_DIR, "wb")
        pickle.dump(data, f)
        f.close()
        # 写日志
        User_Action(cz_usercard,cz_flage,usercard,"解冻用户")
        print("解冻用户[%s],成功！"%(usercard))

# 用户冻结
def User_Frozen(usercard,cz_usercard,cz_flage):
    global data
    # 判断是否为管理员账号
    if cz_flage =="1":
        for x_name in data:
            if x_name["usercard"] == usercard:
                x_name["state"] = "off"
        f = open("%s/config/user_acc.txt" % BASE_DIR, "wb")
        pickle.dump(data, f)
        f.close()
        # 写日志
        User_Action(cz_usercard,cz_flage,usercard,"冻结用户")
        print("冻结用户[%s],成功！"%(usercard))
# 用户删除
def User_del(usercard,cz_usercard,cz_flage):
    global data
    # 判断是否为管理员账号
    if cz_flage =="1":
        for index,x_name in enumerate(data):
            if x_name["usercard"] == usercard:
                del data[index]
        f = open("%s/config/user_acc.txt" % BASE_DIR, "wb")
        pickle.dump(data, f)
        f.close()
        # 写日志
        User_Action(cz_usercard,cz_flage,usercard,"删除用户")
        print("删除用户[%s],成功！"%(usercard))

#用户查询
def Select_User():
    for x_name in data:
        if x_name["flage"] =="1":
            user_type ="管理员"
        else:
            user_type= "信用卡用户"
        print("-"*100)
        print("用户类型:[%s],卡号:[%s],信用授予额度:[%s]元,信用卡当前余额:[%s]元,账单日:[%s]号"
              %(user_type,x_name["usercard"],x_name["total_money"],x_name["new_money"],x_name["Repayment_Date"]))
# 信用卡额度调整
def card_limit(usercard,money,cz_usercard,cz_flage):
    global data
    for x_name in data:
        if x_name["usercard"] == usercard:
            if x_name["total_money"] + money >= 0:
                x_name["total_money"] += money
                x_name["new_money"] += money
                User_Action(cz_usercard,cz_flage,usercard,"调整信用卡额度",money)
                print("调整信用卡[%s],额度成功！"%(usercard))
            else:
                print("信用卡可用额度不能为负数！")
    f = open("%s/config/user_acc.txt" % BASE_DIR, "wb")
    pickle.dump(data, f)
    f.close()

