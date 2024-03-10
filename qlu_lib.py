import requests
import time
import pytz
import datetime

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4706.0 Safari/537.36 Edg/98.0.1084.0",
    "Referer": "http://yuyue.lib.qlu.edu.cn"
}


# 获取东八区日期
def get_time(addday=0):
    time_now = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone("Asia/Shanghai"))
    time_now = time_now + datetime.timedelta(days=addday)
    dt = time_now.strftime("%Y-%m-%d")
    hm = time_now.strftime("%H:%M")
    return [dt, hm]


def is_available(count_list):
    if count_list[0] == 0:
        return False
    for count in count_list:
        if count is None:
            return False
    if count_list[0] == count_list[1]:
        return False
    return True


def query(time):
    url = "http://yuyue.lib.qlu.edu.cn/api.php/areas/1"
    response = requests.request("GET", url)
    PHPSESSID = ";".join('='.join(tup) for tup in response.cookies.items())
    total_url = "http://yuyue.lib.qlu.edu.cn/api.php/areas/0/date/" + time[0]
    # 或许在图书馆崩了的时候有帮助
    try:
        headers["Cookie"] = PHPSESSID
        total_info = requests.get(total_url, headers=headers, timeout=0.8)
    except:
        return [{'area_name': "当前响应过慢，不予访问，减少图书馆压力"}], [
            {'area_name': "当前响应过慢，不予访问，减少图书馆压力"}], ''

    # 判断是否访问成功
    if total_info.status_code != 200:
        print(total_info.status_code, '图书馆已崩')
        return [{'area_name': "图书馆服务崩溃"}], [{'area_name': "图书馆服务器崩溃"}]
    total_info = total_info.json()
    av_seat_list = []  # 记录每个区域空座信息，便于按楼层输出
    un_seat_list = []  # 记录每个区域非空座信息，便于按楼层输出
    for cd_area in total_info['data']['list']['childArea']:
        if cd_area['parentId'] > 1:
            # is_available其实可以不要了,因为已经排除 None 了
            if is_available([cd_area['TotalCount'], cd_area['UnavailableSpace']]):
                available_num = int(cd_area['TotalCount']) - int(cd_area['UnavailableSpace'])
                av_seat_list.append({'area_id': "%02d" % cd_area['id'], 'area_name': cd_area['name'].ljust(30),
                                     'available_num': available_num})
            else:
                un_seat_list.append(
                    {'area_id': "%02d" % cd_area['id'], 'area_name': cd_area['name'], 'available_num': 0})

    # 按楼层排序
    name_sort = lambda x: x['area_name']
    av_seat_list.sort(key=name_sort)
    un_seat_list.sort(key=name_sort)
    return av_seat_list, un_seat_list, "剩余空座："


def get_lib_seat():
    dt, hm = get_time()
    # 查询总的空座信息
    try:
        av_seat_list, un_seat_list, seat_sign = query(get_time())
    except:
        av_seat_list, un_seat_list, seat_sign = [{'area_name': "暂时无法加载....."}], [
            {'area_name': "暂时无法加载....."}], ''
    return dt, hm, av_seat_list, un_seat_list, seat_sign
