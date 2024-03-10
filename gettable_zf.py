import time
import math
import datetime
import requests
from login_jw import login_jw_in_campus
from SQL_link import insert_SQL, dele, update_SQL
super_list = [False, False, False, 0, '', '', '']


def get_today_time(start_date):
    today = datetime.date.today()
    delta = today - start_date
    week_number = delta.days // 7 + 1
    weekday = today.weekday() + 1
    return week_number, weekday


def get_table_zf(start_date):
    # 教务系统查教室的网站
    week_number, weekday = get_today_time(start_date)
    url0 = 'https://jw.qlu.edu.cn/jwglxt/cdjy/cdjy_cxKxcdlb.html?doType=query&gnmkdm=N2155'
    # 请求头初始化
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Cookie': login_jw_in_campus(super_list[5], super_list[6])
    }
    # 周次ID计算
    zcd_list = [2 ** (i - 1) for i in range(week_number, week_number + 1)]

    # 一周七天
    # xgj_list = list(range(1, 8))

    # 一周中的周几
    xgj_list = [weekday]

    # 每节课的ID
    # [3]第一节，[12]第二节，[48]第三节，[192]第四节，[768]晚910节，[15]上午，[240]下午，[1792]整个晚上，[2047]全天
    jcd_list = [3, 12, 48, 192, 768, 15, 240, 1792, 2047]

    # 校区ID
    # [1]长清 [3]历城  [4]菏泽  [zc]彩石 [NH]上合园区
    xqh_list = [1, 3, 4, 'zc', 'NH']

    #  ##########是否进行清空表单################
    dele(super_list[0])
    #  #######################################

    # 更新数据库
    for xqh in xqh_list:
        for zcd in zcd_list:
            for xqj in xgj_list:
                for jcd in jcd_list:
                    timestamp = int(time.time() * 1000)
                    data = {
                        'fwzt': 'cx',
                        'xqh_id': xqh,
                        'xnm': '2023',
                        'xqm': '12',
                        'cdlb_id': '05',
                        'cdejlb_id': '',
                        'qszws': '',
                        'jszws': '',
                        'cdmc': '',
                        'lh': '',
                        'jyfs': '0',
                        'cdjylx': '',
                        'sfbhkc': '',
                        'zcd': zcd,
                        'xqj': xqj,
                        'jcd': jcd,
                        '_search': 'false',
                        'nd': timestamp,
                        'queryModel.showCount': '200',
                        'queryModel.currentPage': '1',
                        'queryModel.sortName': 'cdbh',
                        'queryModel.sortOrder': 'asc',
                        'time': '1'
                    }
                    response = requests.post(url0, data=data, headers=headers)
                    response_json = response.json()
                    cdmc_values = [item['cdmc'] for item in response_json['items']]
                    row = [f'{xqh}_{int(math.log(zcd, 2)) + 1}_{xqj}_{jcd}', ','.join(cdmc_values)]
                    data = {
                        'name': row[0],
                        'room': row[1]
                    }
                    # ###########是否进行插入数据#######
                    insert_SQL(data, super_list[1])
                    # ###############################
                    print(data)


def updategg(contect, que):
    # 公告数据
    data = {
        'name': 'message',
        'room': contect
    }
    # 更新公告
    if que:
        update_SQL(data)
        print("公告内容已经更新！")
    else:
        print("公告内未更新！")
