import pymysql
import random


def connect_database():
    # 打开数据库连接
    connect = pymysql.connect(
        host='',
        port=,
        user='',
        password='',
        db="",
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )

    return connect


# 清空数据库课表数据【危险函数】
def dele(in_delde):
    if in_delde:
        connect = connect_database()
        cursor = connect.cursor()  # 获取游标
        sql = 'TRUNCATE TABLE newclassroom;'
        cursor.execute(sql)
        connect.commit()


# 插入课表数据进入数据库
def insert_SQL(data, inda):
    if inda:
        connect = connect_database()
        cursor = connect.cursor()
        sql = "INSERT INTO newclassroom (name, room) VALUES (%s, %s)"
        cursor.execute(sql, (data['name'], data['room']))
        connect.commit()
        print("数据插入成功")


# 插入男生纸条信息
def man_insert_SQL(data):
    connect = connect_database()
    cursor = connect.cursor()
    sql = "INSERT INTO man (data, name) VALUES (%s, %s)"
    cursor.execute(sql, (data['dat'], data['name']))
    connect.commit()
    print("数据插入成功")


# 插入女生纸条信息
def women_insert_SQL(data):
    connect = connect_database()
    cursor = connect.cursor()
    sql = "INSERT INTO women (data, name) VALUES (%s, %s)"
    cursor.execute(sql, (data['dat'], data['name']))
    connect.commit()
    print("数据插入成功")


# 查询数据库
def query_course_by_section(section_input):
    connect = connect_database()
    cursor = connect.cursor()
    sql = f"SELECT name, room FROM newclassroom WHERE name = '{section_input}'"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result is not None:
        course = result['room']
        if len(course) == 0:
            return "撞大运了，没有空教室呦！"
        else:
            return course
    else:
        return "嘿嘿嘿,兄弟你看看你选错了吗"


# 更新公告
def update_SQL(data):
    connect = connect_database()
    cursor = connect.cursor()
    sql = "UPDATE newclassroom SET room = %s WHERE name = %s"
    cursor.execute(sql, (data['room'], data['name']))
    connect.commit()


def man_random_SQL():
    connect = connect_database()
    cursor = connect.cursor()
    sql = "SELECT COUNT(*) FROM man"
    cursor.execute(sql)
    result = cursor.fetchone()
    dataint = int(result['COUNT(*)'])
    if dataint == 0:
        return "很抱歉，这是空的箱子"
    else:
        random_limit = random.randint(0, dataint - 1)
        query = "SELECT * FROM man LIMIT %s, 1" % random_limit
        cursor.execute(query)
        result = cursor.fetchone()
        new_string = result['data'].replace(",", "，")
        course = result['name'] + "," + new_string
        return course


def women_random_SQL():
    connect = connect_database()
    cursor = connect.cursor()
    sql = "SELECT COUNT(*) FROM women"
    cursor.execute(sql)
    result = cursor.fetchone()
    dataint = int(result['COUNT(*)'])
    if dataint == 0:
        return "很抱歉，这是空的箱子"
    else:
        random_limit = random.randint(0, dataint - 1)
        query = "SELECT * FROM women LIMIT %s, 1" % random_limit
        cursor.execute(query)
        result = cursor.fetchone()
        new_string = result['data'].replace(",", "，")
        course = result['name'] + "," + new_string
        return course


def mandele():
    connect = connect_database()
    cursor = connect.cursor()  # 获取游标
    sql = 'TRUNCATE TABLE man;'
    cursor.execute(sql)
    connect.commit()


def womendele():
    connect = connect_database()
    cursor = connect.cursor()  # 获取游标
    sql = 'TRUNCATE TABLE women;'
    cursor.execute(sql)
    connect.commit()
