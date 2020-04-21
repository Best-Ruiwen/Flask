#!/usr/bin/python3
import sqlite3


def get_data(node, query_time=0):
    cx = sqlite3.connect('data.db')
    cu = cx.cursor()

    # 业务代码
    data = []
    time_data = []
    if query_time == 0:
        cu_ret = cu.execute('select data from {}'.format(node))
        for item in cu_ret:
            data.append(item[0])

        cu_ret = cu.execute('select time from {}'.format(node))
        for item in cu_ret:
            time_data.append(item[0])

    else:
        cu_ret = cu.execute('select data from {} where time>{}'.format(node, query_time))
        for item in cu_ret:
            data.append(item[0])

        cu_ret = cu.execute('select time from {} where time>{}'.format(node, query_time))
        for item in cu_ret:
            time_data.append(item[0])
            
    cu.close()
    cx.close()
    return data, time_data


def write_data(node, time_data, data):
    cx = sqlite3.connect('data.db')
    cu = cx.cursor()

    # 业务代码
    cu.execute('insert into '+node+' values({},{})'.format(time_data, data))
    # 业务代码

    cx.commit()
    cu.close()
    cx.close()


def get_table(username):
    cx = sqlite3.connect('data.db')
    cu = cx.cursor()

    ret = []
    # 业务代码
    cu.execute("select id from userinfo where username=\'{}\'".format(username))  # 根据用户名获取用户ID
    ret_user_id = cu.fetchall()
    if len(ret_user_id):
        cu.execute("select device_id from user_device where"
                   " user_id = \'{}\'".format(ret_user_id[0][0]))  # 根据用户ID获取设备ID
        ret_device_id = cu.fetchall()

        if len(ret_device_id):      # 根据设备ID获取设备名称
            for item in ret_device_id:
                cu.execute("select devicename from deviceinfo where id={}".format(item[0]))
                ret_device_name = cu.fetchall()
                ret.append(ret_device_name[0][0])
        else:
            cu.close()
            cx.close()
            return 0
    # 业务代码

    cu.close()
    cx.close()
    return ret


def login(username, password):  # 从数据库中读取username和password并验证
    cx = sqlite3.connect('data.db')
    cu = cx.cursor()

    try:
        # 使用用户名验证
        cu.execute("select password from userinfo where username = \'{}\'".format(username)) 
        cu_ret = cu.fetchall()
        if len(cu_ret):  
            if cu_ret[0][0] == password:
                cu.close()
                cx.close()
                return 1  # 用户名验证通过
            else:  
                cu.close()
                cx.close()
                return 0   # 验证失败

        # 使用邮箱验证
        cu.execute("select password from userinfo where email = \'{}\'".format(username)) 
        cu_ret = cu.fetchall()
        if len(cu_ret):  
            if cu_ret[0][0] == password:
                cu.execute("select username from userinfo where email = \'{}\'".format(username)) 
                ret = cu.fetchall()
                cu.close()
                cx.close()
                return ret[0][0]  # 邮箱验证通过，返回用户名
            else:  
                cu.close()
                cx.close()
                return 0   # 验证失败

        return 0
    except:
        cu.close()
        cx.close()
        return -1    # 未注册


def pie_handler(data):
    low = middle = high = 0
    for item in data:
        if item < 18:
            low += 1
        elif item > 25:
            high += 1
        else:
            middle += 1
    pie = []
    if low:
        pie.append(low)
    else:
        pie.append(0)

    if middle:
        pie.append(middle)
    else:
        pie.append(0)

    if high:
        pie.append(high)
    else:
        pie.append(0)
    return pie


def add_device(table, username):
    tables = get_table(username)
    if table in tables:
        return '您已经添加过该设备！'   # 该用户名下已经添加了该设备

    cx = sqlite3.connect('data.db')
    cu = cx.cursor()

    cu.execute("select devicename from deviceinfo")
    cu_ret = cu.fetchall()
    tables = []
    for item in cu_ret:
        tables.append(item[0])
    if table in tables:
        cu.close()
        cx.close()
        return '设备名已经存在！'

    cu.execute("create table {}(time float not null,"
               "data float, not null)".format(table))
    cu.execute("insert into deviceinfo values(null,{})".format(table))

    cu.execute("select id from userinfo where username=\"{}\"".format(username))
    userID=cu.fetchall()[0][0]
    cu.execute("select id from deviceinfo where devicename=\"{}\"".format(table))
    deviceID=cu.fetchall()[0][0]
    cu.execute("insert into user_device values({}, {})".format(userID, deviceID))

    cx.commit()
    cu.close()
    cx.close()
    return '添加成功'


# 函数功能:从数据库中删除对应用户的设备
def delete_device(username, device):
    cx = sqlite3.connect('data.db')
    cu = cx.cursor()

    # 删除记录
    cu.execute("select id from userinfo where username=\"{}\"".format(username))
    userID=cu.fetchall()[0][0]
    cu.execute("select id from deviceinfo where devicename=\"{}\"".format(device))
    deviceID=cu.fetchall()[0][0]
    cu.execute("delete from user_device where user_id={} and device_id={}".format(userID, deviceID))

    # 删除表 
    cu.execute("drop table {}".format(device))

    cx.commit()
    cu.close()
    cx.close()


# 判断是否已经注册
def isregister(email):
    cx = sqlite3.connect('data.db')
    cu = cx.cursor()
    try:
        cu.execute("select id from userinfo where email=\"{}\"".format(email))
        userID=cu.fetchall()[0][0]
        cu.close()
        cx.close()
        return True  # 邮箱已经存在
    except:
        cu.close()
        cx.close()
        return False    # 未注册的邮箱和用户名


# 注册
def register(username, password, email):
    cx = sqlite3.connect('data.db')
    cu = cx.cursor()
    try:
        cu.execute("insert into userinfo values(null, \"{}\", \"{}\", \"{}\")".format(username, password, email))
        cx.commit()
        cu.close()
        cx.close()
        return True
    except:
        cu.close()
        cx.close()
        return False


# 判断设备是否注册
def isregister_device(device):
    cx = sqlite3.connect('data.db')
    cu = cx.cursor()
    try:
        cu.execute("select id from deviceinfo where devicename=\"{}\"".format(device))
        device_ID=cu.fetchall()[0][0]
        cu.close()
        cx.close()
        return True  # 已经注册的设备
    except:
        cu.close()
        cx.close()
        return False  # 未注册的设备


# 重置密码时，写入密码
def resetpasswd(email, password):
    cx = sqlite3.connect('data.db')
    cu = cx.cursor()
    try:
        cu.execute("update userinfo set password=\"{}\" where email=\"{}\"".format(password, email))
        cx.commit()
        cu.close()
        cx.close()
        return True
    except:
        cu.close()
        cx.close()
        return False


if __name__ == '__main__':
    print('Filename:datahandler.py')
    print('Function:Read data from data base or write data to data base')
