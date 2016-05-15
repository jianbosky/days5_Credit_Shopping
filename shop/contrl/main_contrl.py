#!/usr/bin/env python3.5
# -*-coding:utf8-*-
import sys,os,pickle
ROOT_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
import os
import sys
from ATM.API.atm_api import User_Pay_Api
f = open("%s/config/user_acc.txt" % ROOT_DIR, "rb")
data = pickle.loads(f.read())
f.close()
def sale(username):
    print('欢迎用户%s进入购物商城!' % (username))
    print("以下是商品信息，请按键选择商品，进入购买界面！")
    item = {1:{"苹果":"4"},2:{"香焦":"2"},3:{"桔子":"3"},4:{"菠萝":"3"}}
    for k,v in item.items():
        for x,y in v.items():
            print("%s、%s：%s元/斤"%(k,x,y))

    num =int(input("请输入要购买商品的编号：").strip())
    if num in item:
        for k1 in item[num]:
            v1=(item[num][k1])
            shulian = int(input("你选择的是'%s'单价为:%s元/斤，请输入要购买的数量，单位（斤）:" %(k1,v1)).strip())
            # 调用购物车方法
            gouwuche(username, k1, shulian,num)
            xy=input("加入购物车成功，查看购车请按“1”结算请选择“2”还需购买请选择“3”").strip()
            if xy == "1":
                return show(username,item)
            elif xy == "2":
                return jieshan(username,item)
            elif xy == "3":
                return sale(username)
    else:
        print("输入错误,请重新输入\n\n")
        return sale(username)
def gouwuche (username, k1, shulian,num):
    xz = input("你选择了'%s',数量%s斤，是|否确认加入购物车:：是｜否" %(k1,shulian)).strip()
    if xz == "是":
        # 判断是否存在该用户的购物车文件
        gw = "%s %s\n" % (num, shulian)
        if os.path.isfile("%s.txt" % username)  == True:
            # 如果是购物车存在则修改
            with open("%s.txt" % username, "r")as xf:
                lines = xf.readlines()
                l = len(lines)
                for i in range(l):
                    # 如果购物车存在该条数据则进行修改
                    if num == int(lines[i].split()[0]):
                        old_ = int(lines[i].split()[1])
                        new_ = old_ + shulian
                        # 如果该记录是最后修改数据后面不换行
                        if i == l:
                            new = "%s %s" %(num,new_)
                        # 否则换行
                        else:
                            new = "%s %s\n" %(num,new_)
                        # 修改原数据
                        lines[i] = new
                        # 跳出for循环写入修改数据
                        break
                # 如果购物车不存在该条数据则在记录最后进行新增
                else:
                    lines.append(gw)
                # 将更改后的数据写入文件
                with open("%s.txt" % username, "w")as f:
                    f.writelines(lines)
                return 0
        else:
            with open("%s.txt" % username, "w") as f:
                f.writelines(gw)
            return 0
    elif xz == "否":
        return sale(username)
    else:
        return gouwuche(username, k1, shulian,num)
def show(username,item):
    with open("%s.txt"%username,"r") as f:
        data = f.readlines()
        total = 0
        for i in data:
            xnum,xdata = i.strip().split()
            ixnum = int(xnum)
            ixdata = int(xdata)
            for i in item[ixnum]:
                v2 = item[ixnum][i]
                total += (int(v2) * ixdata)
                print("""
                 －－－－－－－－－－－－－－－－－－－－－－
                 商品编号 商品名称   商品单价   商品数量   商品金额
                     %s        %s         %s        %s       %d """%(ixnum,i,v2,ixdata,(int(v2) * ixdata)))

    print("你的购物车总金额为:%s 元." % total)
    tell2=input("请选择：1、清空购物车，2、返回继续购物，3、商品结算 ：")
    if tell2 == "1":
        os.remove("%s.txt"%username)
        print("购物车已清空，请重新购物")
        sale(username)
    elif tell2 == "2":
        sale(username)
    elif tell2 == "3":
        jieshan(username,item)
    else:
        show(username,item)
def jieshan(username,item):
    with open("%s.txt"%username,"r") as f:
        data = f.readlines()
        total = 0
        for i in data:
            xnum,xdata = i.strip().split()
            ixnum = int(xnum)
            ixdata = int(xdata)
            for i in item[ixnum]:
                v2 = item[ixnum][i]
                total += (int(v2) * ixdata)
    print("当前正调用信用卡接口结账：")
    input_usercard = int(input("请输入信用卡卡号"))
    input_passwd =  input("请输入信用卡密码").strip()
    sall = User_Pay_Api(input_usercard,input_passwd,total)
    if sall ==2:
        print("你购物车内的商品总价格为：%s元，已超过你的可用金额,请返回购物车修改商品" %(total))
        show(username,item)
    elif sall == 3:
        show(username,item)
    elif sall == 4:
        jieshan(username,item)
    elif sall == None:
        # 清空购物车
        os.remove("%s.txt"%username)
        tell = input("感谢你的选购，请选择是否继续购买：是｜否")
        if tell == "是":
            sale(username)
        else:
            print("谢谢光临，再见！")
            sys.exit()
