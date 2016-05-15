#!/usr/bin/env python3.5
# -*-coding:utf8-*-
'''
购物商城系统数据文件说明：
  数据存储目录为 config
  1、该目录下 lock_user.txt 为用户锁定控制文件 如此文件中含有的用户名禁止登陆，同时被锁定的用户保存在此文件中
  2、该目录下user_acc.txt 为账户数据文件
  账号  123456  密码 111111
  账号  456789  密码 111111
  账号  147258  密码 111111
'''
import sys,os,pickle
ROOT_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

# 导入菜单模块
from shop.contrl.main_contrl import sale

f = open("%s/shop/config/user_acc.txt" % ROOT_DIR, "rb")
data = pickle.loads(f.read())
f.close()
print("""
        欢迎您进入购物商城，请登陆后购买商品！
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
                print("该账号已被冻结！")
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
        usercard = int(input("请输入用户密码:"))
        for x_name in open("%s/shop/config/lock_user.txt" % ROOT_DIR).readlines():
            # 将用户名 以换行符分割 去左右空格后存储于列表中
            lock_name = [lock_name for lock_name in x_name.strip().split("\n")]
            # 对用户输入的用户名进行判断是否存在于被锁定列表中
            for card in lock_name:
                if usercard == int(card):
                    print("您的账号已被锁定！")
                    # 退出程序
                    sys.exit()
        else:
            password = input("请输入用户密码：").strip()
            # 调用LOGIN函数
            flages = login(usercard, password)

        if flages == True:
            break
    if i > 2 and flages == False:
        # 用户输入错误次数达到3次且没有认证成功，被锁定
        print("您的账号已被锁定！")
        # 将锁定的用户名写入文件中，永久保存
        f = open("config/lock_user.txt", "a")
        # 将被锁定的用户名以换行的形式进行存储
        f.write("%s\r" % usercard)
        # 关闭写文件，结束程序
        f.close()
    # 登陆成功后
    if flages == True:
        return sale(usercard)

if __name__ == '__main__':
    # 运行主函数
    main()

