#!/usr/bin/python3
from .base import Connect


def get_data(node, query_time=0):
    """
    :param node: 指节点名称
    :param query_time: 查询时间范围
    :return:
    """
    data = []
    time_data = []
    with Connect() as cu:
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
    return data, time_data


def write_data(node, time_data, data):
    with Connect() as cu:
        cu.execute('insert into {} values({},{})'.format(node, time_data, data))


# 根据用户名获取用户的设备表，返回设备列表
def get_table(username):
    tables = []
    with Connect() as cu:
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
                    tables.append(ret_device_name[0][0])
            else:
                return 0
    return tables


def login(username, password):
    """
    :param username:
    :param password:
    :return: 1代表用户名验证通过,
             -1代表验证失败,
             0代表用户和邮箱验证都失败了，
             其他代表邮箱验证成功，返回了邮箱地址
    """
    with Connect() as cu:
        # 检查是否是使用用户名登陆
        cu.execute("select password from userinfo where username = \'{}\'".format(username))
        cu_ret = cu.fetchall()
        if len(cu_ret):
            if cu_ret[0][0] == password:
                return 1   # 用户名验证成功
            else:
                return 0   # 用户名验证失败

        # 尝试邮箱验证
        cu.execute("select password from userinfo where email = \'{}\'".format(username))
        cu_ret = cu.fetchall()
        if len(cu_ret):
            if cu_ret[0][0] == password:    # 邮箱验证通过
                cu.execute("select username from userinfo where email = \'{}\'".format(username))
                ret = cu.fetchall()
                return ret[0][0]
            else:
                return 0   # 邮箱验证失败
    # 未注册的邮箱
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


def add_device(table, username, ip, ip_type):

    """
    :param table表示的实际上是节点名，以该节点的名字来创建表，
    :param ip_type表示IP地址是ipv4还是ipv6
    """

    tables = get_table(username)
    if tables:
        if table in tables:
            return '您已经添加过该设备！'

    with Connect() as cu:
        cu.execute("select devicename from deviceinfo")
        cu_ret = cu.fetchall()
        tables = []
        if len(cu_ret):
            for item in cu_ret:
                tables.append(item[0])
        if table in tables:
            return '设备名已经存在！'

        cu.execute("create table {}(time float not null, data float not null)".format(table))  # 创建表
        cu.execute("insert into deviceinfo values(null,\'{}\', \'{}\', \'{}\')".format(table, ip, ip_type))  # 设备信息表
        cu.execute("select id from userinfo where username=\"{}\"".format(username))    # 获取用户名对应的ID
        userID = cu.fetchall()[0][0]
        cu.execute("select id from deviceinfo where devicename=\"{}\"".format(table))   # 获取设备ID
        deviceID = cu.fetchall()[0][0]
        cu.execute("insert into user_device values({}, {})".format(userID, deviceID))  # 写入映射表
        return '添加成功'


def delete_device(username, device):
    with Connect() as cu:
        cu.execute("select id from userinfo where username=\"{}\"".format(username))
        userID = cu.fetchall()[0][0]
        cu.execute("select id from deviceinfo where devicename=\"{}\"".format(device))
        deviceID = cu.fetchall()[0][0]
        cu.execute("delete from deviceinfo where devicename=\"{}\"".format(device))
        cu.execute("delete from user_device where user_id={} and device_id={}".format(userID, deviceID))
        cu.execute("drop table {}".format(device))


def getipBydeviceName(device):
    with Connect() as cu:
        cu.execute("select ip from deviceinfo where devicename=\"{}\"".format(device))
        ip = cu.fetchall()[0][0]
        cu.execute("select status from deviceinfo where devicename=\"{}\"".format(device))
        status = cu.fetchall()[0][0]
    return ip, status


def isregister(email):
    with Connect() as cu:
        cu.execute("select id from userinfo where email=\"{}\"".format(email))
        userID = cu.fetchall()[0][0]

    # 如果userID的长度为0，则代表没有注册，就会返回False
    return bool(len(userID))


def register(username, password, email):
    try:
        with Connect() as cu:
            cu.execute("insert into userinfo values(null, \"{}\", \"{}\", \"{}\")".format(username, password, email))
        return True
    except:
        return False


def isregister_device(device):
    with Connect() as cu:
        cu.execute("select id from deviceinfo where devicename=\"{}\"".format(device))
        device_ID = cu.fetchall()[0][0]

    # 如果device_ID的长度为0，则代表没有注册，就会返回False
    return bool(len(device_ID))


def resetpasswd(email, password):
    try:
        with Connect() as cu:
            cu.execute("update userinfo set password=\"{}\" where email=\"{}\"".format(password, email))
        return True
    except:
        return False


def rectify(node, ip, ip_type):
    try:
        with Connect() as cu:
            cu.execute("update deviceinfo set ip=\"{}\", status=\"{}\" where devicename=\"{}\"".format(ip, ip_type, node))
        return True
    except:
        return False


def getmail(username):
    with Connect() as cu:
        cu.execute("select email from userinfo where username=\'{}\'".format(username))
        email = cu.fetchall()[0][0]
    return email


def create_database():
    time = [1578489630.80251, 1578489714.44998, 1578489722.58172, 1578489730.0516, 1578489737.00513]
    data = [10.4574078430068, 17.0097587311147, 11.5051689617662, 20.5521855823856, 18.261248777006]
    with Connect() as cu:
        # 创建用户信息表
        cu.execute("create table userinfo ( \
            id integer primary key autoincrement, \
            username char(10) not null, \
            password char(20) not null, \
            email char(50) not null);")
        # 创建设备信息表
        cu.execute("create table deviceinfo ( \
            id integer primary key autoincrement, \
            devicename char(20) not null,\
            ip char(128) not null, \
            status char not null);")
        # 创建映射表
        cu.execute("create table user_device ( \
            user_id int not null, \
            device_id not null);")
        cu.execute("create table node_1034 ( \
            time float not null, \
            data float not null \
            );")
        for t, d in zip(time, data):
            cu.execute("insert into node_1034(time, data) values({}, {})".format(t, d))


if __name__ == '__main__':
    print('Filename:datahandler.py')
    print('Function:Read data from data base or write data to data base')
