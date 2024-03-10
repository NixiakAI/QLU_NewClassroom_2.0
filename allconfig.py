import gettable_zf
import datetime

today = datetime.date.today()
to = str(today.month) + '.' + str(today.day)

gettable_zf.start_date = datetime.date(2024, 2, 26)  # 定义开学时间
gettable_zf.super_list[0] = False  # 是否清除全部的数据，数据库需要重置的时候使用，多用在学期开始
gettable_zf.super_list[1] = False  # 是否进行更新数据库
gettable_zf.super_list[2] = False  # 是否更新公告
gettable_zf.super_list[3] = 0  # 空参数
gettable_zf.super_list[4] = "空教室群号：719708676。数据更新至" + to  # 公告的内容
gettable_zf.super_list[5] = ""  # 教务系统账号
gettable_zf.super_list[6] = ""  # 教务系统密码

gettable_zf.get_table_zf(gettable_zf.start_date)
gettable_zf.updategg(gettable_zf.super_list[4], gettable_zf.super_list[2])
