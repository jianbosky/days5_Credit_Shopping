# days5_Credit_Shopping
购物商城+信用卡管理支付系统

一、系统介绍
	本系统分两部分，一部分是购物商城，提供账号登陆、锁定、选购商品、加入购物车，调用信用卡结账
一部分是信用卡系统，提供信用卡与管理员同时登陆、账号锁定、解冻卡号、账单查询，取现、转账、余额调整、每日利息计算、取现手续费收取、ATM操作日志等功能

二、系统原理

1、文件说明：
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

购物商城系统数据文件说明：
  数据存储目录为 config
  1、该目录下 lock_user.txt 为用户锁定控制文件 如此文件中含有的用户名禁止登陆，同时被锁定的用户保存在此文件中
  2、该目录下user_acc.txt 为账户数据文件
  账号  123456  密码 111111
  账号  456789  密码 111111
  账号  147258  密码 111111
2、系统基本设计原理

	购物商城系统： 用户登陆系统－选购商品－加入购物车－查看购物车－结算－调用信用卡支付接口－输入信用卡卡号及密码－结算成功、或失败
	信用卡系统： 1、用户登陆－判断是信用卡用户还是管理员－－信用卡用户－显示查询、取现、转账、账单查询、还款等功能－根据不同选择调用不同的函数，并做好日志记录及消费明细记录； 
		     2、如果是管理员－显示ATM日志查询、账户管理、信用额度调整等功能－账户管理－显示添加卡号、删除用户、冻结用户、解冻用户等功能，据据不同选择调用不同的函数并执行；
		     3、信用卡系统后台自动结转账单、根据不同的账单日期生成本月交易流水，同时如果是取现自动提取手续费，到期未还款自动计算每笔消费所累计产生的利息等，同时为保证每天只计算一次利息对各功能做了特殊处理，以保证所有数据的准备性与无重复性，后台利息处理系统也记录了每天产生的利息总和，但没有在前后显示每个账号每天利息和，如需要可以显示出来，前台只在每笔消费中体现出每笔过期未还产生利息的总和

三、开源网址：
       https://github.com/jianbosky/days5_Credit_Shopping