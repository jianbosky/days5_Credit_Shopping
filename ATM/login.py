#!/usr/bin/env python3.5
# -*-coding:utf8-*-
'''
信用卡系统数据文件说明：
  数据存储目录为 config
  1、该目录下 calculation_log.txt 为利息初始化计算文件 主要用来记录每天所产生的利息，
  同时防止隔天漏计算或当天重复计算，如果今天已计算，还需要计算 请删除该文件。
  2、该目录下 lock_user.txt 为用户锁定控制文件 如此文件中含有的用户名禁止登陆，同时被锁定的用户保存在此文件中
  3、该目录下user_acc.txt 为信用卡账户数据文件，保存有管理员用户和信用卡用户 ，同时将 卡号、密码、等级、账单日、
  可用信用余额和 总授予信用额度保存在此文件中
  4、该目录下 user_list.txt 用来保存用户消费明细，同时将利息 、是否出账单、是否还清等一并记入当中，
  所有利息与账单均以此文件相关联
  5、该目录下user_log.txt 用户记录管理员增加用户、删除用户、冻结用户、调整信用额度，用户取现，还款、转账、消费等所有日志

  管理员账号  123456  密码 111111
  信用卡账号  456789  密码 111111
  信用卡账号  147258  密码 111111
'''
import sys,os,pickle
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
# 导入菜单模块
from contrl.atm_main import menu
# 导入利息计算模块
from config.settings import computer

f = open("%s/config/user_acc.txt" % BASE_DIR, "rb")
data = pickle.loads(f.read())
f.close()
print("""
        欢迎您进入ATM 银行，请登陆后进行操作！
""")
# 登陆函数
def login(usercard, password):
    global data
    for user_data in data:
        if user_data["usercard"] == usercard and user_data["password"] == password:
            # 判断该信用卡是否被冻结
            if user_data["state"] == "on":
                print("登陆成功！")
                return True
            else:
                print("该信用卡已被冻结！")
                sys.exit()
    else:
        print("登陆失败（账号或密码错误）！")
        return False
# 主运算控制函数
def main():
    global data
    i = 0
    flages = False
    while i < 3 and flages ==False:
        i += 1
        usercard = int(input("请输入信用卡卡号:"))
        for x_name in open("config/lock_user.txt").readlines():
            # 将用户名 以换行符分割 去左右空格后存储于列表中
            lock_name = [lock_name for lock_name in x_name.strip().split("\n")]
            # 对用户输入的用户名进行判断是否存在于被锁定列表中
            for card in lock_name:
                if usercard == int(card):
                    print("您的信用卡已被锁定！")
                    # 退出程序
                    sys.exit()
        else:
            password = input("请输入信用卡密码：").strip()
            # 调用LOGIN函数
            flages = login(usercard, password)

        if flages == True:
            break
    if i > 2 and flages == False:
        # 用户输入错误次数达到3次且没有认证成功，被锁定
        print("您的信用卡已被锁定！")
        # 将锁定的用户名写入文件中，永久保存
        f = open("config/lock_user.txt", "a")
        # 将被锁定的用户名以换行的形式进行存储
        f.write("%s\r" % usercard)
        # 关闭写文件，结束程序
        f.close()
    # 登陆成功后
    if flages == True:
        for user_data in data:
            if user_data["usercard"] == usercard:
                # 调用显示菜单函数
                menu(usercard,user_data["flage"])

if __name__ == '__main__':
    # 到期还款利息计算函数 ，注：如果当天已计算利息，如果通过调整电脑日期进行消费
    # 或还需要今天计算利息请把 config目录下calculation_log.txt文件删除
    computer()
    # 运行主函数
    main()

