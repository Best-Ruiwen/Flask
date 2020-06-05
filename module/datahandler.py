#!/usr/bin/python3
import sqlite3
def get_data(node, query_time=0):
    cx = sqlite3.connect('data.db')
    cu = cx.cursor()
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
    cu.execute('insert into {} values({},{})'.format(node,time_data, data))
    cx.commit()
    cu.close()
    cx.close()
def get_table(username):
    cx = sqlite3.connect('data.db')
    cu = cx.cursor()
    ret = []
    cu.execute("select id from userinfo where username=\'{}\'".format(username))  
    ret_user_id = cu.fetchall()
    if len(ret_user_id):
        cu.execute("select device_id from user_device where"
                   " user_id = \'{}\'".format(ret_user_id[0][0]))  
        ret_device_id = cu.fetchall()
        if len(ret_device_id):      
            for item in ret_device_id:
                cu.execute("select devicename from deviceinfo where id={}".format(item[0]))
                ret_device_name = cu.fetchall()
                ret.append(ret_device_name[0][0])
        else:
            cu.close()
            cx.close()
            return 0
    cu.close()
    cx.close()
    return ret
def login(username, password):  
    cx = sqlite3.connect('data.db')
    cu = cx.cursor()
    try:
        cu.execute("select password from userinfo where username = \'{}\'".format(username)) 
        cu_ret = cu.fetchall()
        if len(cu_ret):  
            if cu_ret[0][0] == password:
                cu.close()
                cx.close()
                return 1  
            else:  
                cu.close()
                cx.close()
                return 0   
        cu.execute("select password from userinfo where email = \'{}\'".format(username)) 
        cu_ret = cu.fetchall()
        if len(cu_ret):  
            if cu_ret[0][0] == password:
                cu.execute("select username from userinfo where email = \'{}\'".format(username)) 
                ret = cu.fetchall()
                cu.close()
                cx.close()
                return ret[0][0]  
            else:  
                cu.close()
                cx.close()
                return 0   
        return 0
    except:
        cu.close()
        cx.close()
        return -1   
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
def add_device(table, username, ip, status):
    tables = get_table(username)
    if table in tables:
        return '您已经添加过该设备！'  
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
               "data float, not null)".format(table))  # 创建表
    cu.execute("insert into deviceinfo values(null,{}, {})".format(table, status))  # 设备信息表
    cu.execute("select id from userinfo where username=\"{}\"".format(username))
    userID=cu.fetchall()[0][0]
    cu.execute("select id from deviceinfo where devicename=\"{}\"".format(table))
    deviceID=cu.fetchall()[0][0]
    cu.execute("insert into user_device values({}, {})".format(userID, deviceID))  # 写入映射表
    cx.commit()
    cu.close()
    cx.close()
    return '添加成功'
def delete_device(username, device):
    cx = sqlite3.connect('data.db')
    cu = cx.cursor()
    cu.execute("select id from userinfo where username=\"{}\"".format(username))
    userID=cu.fetchall()[0][0]
    cu.execute("select id from deviceinfo where devicename=\"{}\"".format(device))
    deviceID=cu.fetchall()[0][0]
    cu.execute("delete from user_device where user_id={} and device_id={}".format(userID, deviceID))
    cu.execute("drop table {}".format(device))
    cx.commit()
    cu.close()
    cx.close()
def getipBydeviceName(device):
    cx = sqlite3.connect('data.db')
    cu = cx.cursor()
    cu.execute("select ip from deviceinfo where devicename=\"{}\"".format(device))
    ip = cu.fetchall()[0][0]
    cu.execute("select status from deviceinfo where devicename=\"{}\"".format(device))
    status = cu.fetchall()[0][0]
    cu.close()
    cx.close()
    return ip, status
def isregister(email):
    cx = sqlite3.connect('data.db')
    cu = cx.cursor()
    try:
        cu.execute("select id from userinfo where email=\"{}\"".format(email))
        userID=cu.fetchall()[0][0]
        cu.close()
        cx.close()
        return True  
    except:
        cu.close()
        cx.close()
        return False   
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
def isregister_device(device):
    cx = sqlite3.connect('data.db')
    cu = cx.cursor()
    try:
        cu.execute("select id from deviceinfo where devicename=\"{}\"".format(device))
        device_ID=cu.fetchall()[0][0]
        cu.close()
        cx.close()
        return True 
    except:
        cu.close()
        cx.close()
        return False  
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
def rectify(node, ip, status):
    cx = sqlite3.connect('data.db')
    cu = cx.cursor()
    try:
        cu.execute("update deviceinfo set ip=\"{}\", status=\"{}\" where devicename=\"{}\"".format(ip, status, node))
        cx.commit()
        cu.close()
        cx.close()
        return True
    except:
        cu.close()
        cx.close()
        return False
def getmail(username):
    cx = sqlite3.connect('data.db')
    cu = cx.cursor()
    cu.execute("select email from userinfo where username=\'{}\'".format(username))
    email = cu.fetchall()[0][0]
    cu.close()
    cx.close()
    return email
if __name__ == '__main__':
    print('Filename:datahandler.py')
    print('Function:Read data from data base or write data to data base')
