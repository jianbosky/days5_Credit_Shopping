#!/usr/bin/env python3.5
# -*-coding:utf8-*-
import os
import time
import pickle
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from contrl.views import *
from contrl.management import *
# 打开用户账号信息文件
if os.path.exists(r'%s/config/user_acc.txt'% BASE_DIR):
    f = open("%s/config/user_acc.txt" % BASE_DIR, "rb")
    data_user = pickle.loads(f.read())
    f.close()

def menu (usercard,flage):
    global data_user
    menu_info_user = {"1":"查询余额及可用额度","2":"取现","3":"账户转账","4":"账单查询","5":"信用卡还款","6":"退出"}
    menu_info_admin = {"1":"ATM操作日志查询","2":"信用卡账户管理","3":"用户额度管理","4":"退出"}
    # 管理员
    if flage == "1":
        print("欢迎[%s]登陆ATM银行，你的身份为管理员" %(usercard))
        print("1、%s" % (menu_info_admin["1"]))
        print("2、%s" % (menu_info_admin["2"]))
        print("3、%s" % (menu_info_admin["3"]))
        print("4、%s" % (menu_info_admin["4"]))
        input_number = input("请输入对应的数字编号:").strip()
        if input_number == "1":
            select_log()
            return menu (usercard,flage)
        elif input_number == "2":
            # try:
            print("""
                    1、增加信用卡用户
                    2、冻结信用卡用户
                    3、解冻信用卡用户
                    4、查询信用卡用户
                    5、删除信用卡用户
            """)
            card_input=input("请输入要操作的功能编号：").strip()
            # 增加信用卡用户
            if card_input =="1":
                user_type = input("请输入用户所属类型，1、[管理用户]，2、[信用卡用户]:").strip()
                user_card = int(input("请输入需增加的用户卡号:"))
                user_pwd = input("请输入卡号密码：").strip()
                user_total = int(input("请输入用户信用额度，单位（元）："))
                user_date = input("请输入账单生成日（默认为22号）：").strip()
                if user_card != "" and len(user_type) != 0 and len(user_pwd) != 0:
                    if user_date == "":
                        user_date = 22
                    User_Add(usercard,flage,user_card,user_pwd,user_total,int(user_date),user_type)
                    return menu (usercard,flage)
            # 冻结信用卡用户
            elif card_input =="2":
                usercard_input= input("请输入要冻结的信用卡卡号：").strip()
                if usercard_input != "":
                    User_Frozen(int(usercard_input),usercard,flage)
                    return menu (usercard,flage)
                else:
                    return menu (usercard,flage)
            # 解冻信用卡用户
            elif card_input == "3":
                usercard_input= input("请输入要解冻的信用卡卡号：").strip()
                if usercard_input != "":
                    User_thaw(int(usercard_input),usercard,flage)
                    return menu (usercard,flage)
                else:
                    return menu (usercard,flage)
            # 查询信用卡用户
            elif card_input == "4":
                Select_User()
                return menu (usercard,flage)
            # 删除信用卡用户
            elif card_input == "5":
                usercard_input= input("请输入要删除的信用卡卡号：").strip()
                if usercard_input != "":
                    User_del(int(usercard_input),usercard,flage)
                    return menu (usercard,flage)
                else:
                    return menu (usercard,flage)
        # 用户额度管理
        elif input_number == "3":
            usercard_input = input("请输入要调整额度的信用卡卡号：").strip()
            usermoney_input = input("请输入要调整的信用卡额度,如：－1000 或 1000，:").strip()
            if usercard_input != "" and usermoney_input != "":
                card_limit(int(usercard_input),int(usermoney_input),usercard,flage)
                return menu (usercard,flage)
            else:
                print("输入错误！")
                return menu (usercard,flage)
        # 退出
        elif input_number == "4":
            sys.exit()
        else:
            return menu (usercard,flage)
    # 信用卡用户
    elif flage == "2":
        print("欢迎[%s]登陆ATM银行，请选择您所需要的功能编号 " % (usercard))
        print("1、%s" %(menu_info_user["1"]))
        print("2、%s" %(menu_info_user["2"]))
        print("3、%s" %(menu_info_user["3"]))
        print("4、%s" %(menu_info_user["4"]))
        print("5、%s" %(menu_info_user["5"]))
        print("6、%s" %(menu_info_user["6"]))
        input_number = input("请输入对应的数字编号:").strip()
        # 查询余额及可用额度
        if input_number == "1":
            select_balance(usercard, flage)
            return menu (usercard,flage)
        # 信用卡取现
        elif input_number == "2":
            usermoney_input = int(input("请输入取款金额:"))
            if usermoney_input > 0:
                Take_Money(usercard,usermoney_input,flage)
                return menu (usercard,flage)
            else:
                print("取款金额不能为负数")
                return menu (usercard,flage)
        # 信用卡转账
        elif input_number == "3":
            usercard_input = int(input("请输入转账对方的信用卡卡号："))
            for in_user in data_user:
                if in_user["usercard"] == usercard_input:
                    usermoney_input = int(input("请输入转账金额："))
                    for x_user in data_user:
                        if x_user["new_money"] - usermoney_input >= 0:
                            Transfer(usercard,flage,usercard_input,usermoney_input)
                            return menu (usercard,flage)
                        else:
                            print("转账失败，可用余额不足")
                            return menu (usercard,flage)
            else:
                print("转账对方的信用卡卡号不存在！")
                return menu (usercard,flage)
        # 信用卡账单查询
        elif input_number == "4":
            for x_name in data_user:
                if x_name["usercard"] == usercard:
                    bill_date = x_name["Repayment_Date"]
                    select_bill(usercard,bill_date)
            return menu (usercard,flage)
        # 信用卡还款
        elif input_number == "5":
            usermoney_input = int(input("请输入还款现金的额度："))
            if usermoney_input > 0:
                Card_Payment(usercard,usermoney_input,flage)
                return menu (usercard,flage)
            else:
                print("还款现金金额必须大于0")
                return menu (usercard,flage)
        # 退出
        elif input_number == "6":
            sys.exit()
        else:
            return menu(usercard,flage)
# 查询信用卡额度及可用余额信息


