#!/usr/bin/python3
from .base import Connect
import re


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
                    cu.execute("select device_name from deviceinfo where id={}".format(item[0]))
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
                return 1  # 用户名验证成功
            else:
                return 0  # 用户名验证失败

        # 尝试邮箱验证
        cu.execute("select password from userinfo where email = \'{}\'".format(username))
        cu_ret = cu.fetchall()
        if len(cu_ret):
            if cu_ret[0][0] == password:  # 邮箱验证通过
                cu.execute("select username from userinfo where email = \'{}\'".format(username))
                ret = cu.fetchall()
                return ret[0][0]
            else:
                return 0  # 邮箱验证失败
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
            cu.execute(
                "update deviceinfo set ip=\"{}\", status=\"{}\" where device_name=\"{}\"".format(ip, ip_type, node))
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
        # 创建网关信息表
        cu.execute("create table gateway_info ( \
                            id integer primary key \
                                    autoincrement, \
                            gateway_name char(20) not null \
                                                  unique,\
                            gateway_id char(128) not null, \
                            secret char(48) not null);")
        # 创建映射表
        cu.execute("create table user_gateway ( \
                            user_id int not null, \
                            gateway_id not null);")
        cu.execute("create table node_1034 ( \
                            time float not null, \
                            data float not null \
                            );")
        for t, d in zip(time, data):
            cu.execute("insert into node_1034(time, data) values({}, {})".format(t, d))


# 根据用户名查找设备
def get_devices_by_username(username):
    """
    :param username: 用户名
    :return: {网关：设备}字典
    """
    gateways = get_gateway_by_username(username)
    devices = {}

    for gateway in gateways:
        devices[gateway] = get_device_by_gateway(gateway)

    return devices


def get_gateway_by_username(username):
    """
    :param username:用户名
    :return: 网关列表
    """
    gateway = []
    with Connect() as cu:
        cu.execute("select id from userinfo where username=\"{}\"".format(username))
        user_id = cu.fetchall()[0][0]

        cu.execute("select gateway_id from user_gateway where user_id=\"{}\"".format(user_id))
        gateway_id = cu.fetchall()
        if len(gateway_id):
            for item in gateway_id:
                cu.execute("select gateway_name from gateway_info where id = \"{}\"".format(item[0]))
                temp = cu.fetchall()
                if len(temp):
                    gateway.append(temp[0][0])
    return gateway


def get_device_by_gateway(gateway):
    """
    :param gateway: 网关名(单个网关)
    :return: 该网关下的设备列表
    """
    devices = []
    with Connect() as cu:
        cu.execute("select device_name from \"{}\"".format(gateway))
        device_name = cu.fetchall()
        if len(device_name):
            for device in device_name:
                # 将网关名和设备名分开
                temp = re.sub(gateway + "_", "", device[0])
                devices.append(temp)
        return devices


# 添加网关
def add_gateway_to_user(username, gateway_name):
    """
    :param username: 用户名
    :param gateway_name: 待添加的网关名
    :return: True:添加成功， False:添加失败
    """
    with Connect() as cu:
        try:
            # 数据库中限定了gateway_name唯一，如果使用已被添加的name, 将会报错
            # 更新 gateway_info
            cu.execute("insert into gateway_info(gateway_name) values(\"{}\")".format(gateway_name))

            # 更新user_gateway
            cu.execute("select id from userinfo where username=\"{}\"".format(username))
            user_id = cu.fetchall()[0][0]
            cu.execute("select id from gateway_info where gateway_name=\"{}\"".format(gateway_name))
            gateway_id = cu.fetchall()[0][0]
            cu.execute("insert into user_gateway(user_id, gateway_id) values({}, {})".format(user_id, gateway_id))

            # 创建网关表
            cu.execute(" CREATE TABLE {} (device_name CHAR (40)  PRIMARY KEY \
                                                                 UNIQUE \
                                                                 NOT NULL, \
                                          device_id   CHAR (128) NOT NULL)".format(gateway_name))
            return True
        except:
            return False


def add_device_to_gateway(device_name, device_id, gateway):
    """
    :param device_name: 设备名
    :param device_id: 设备ID，一般是mac地址
    :param gateway: 网关名
    :return:
    """
    with Connect() as cu:
        try:
            # 数据中限定了设备名唯一，如果设备名已经被使用，就会报错
            insert_name = gateway + '_' + device_name
            cu.execute("insert into {}(device_name, device_id) values(\"{}\", \"{}\");".format(gateway, insert_name, device_id))

            # 创建数据表，数据表的名字为gateway_device_name，以确保表的名字唯一
            table_name = gateway + '_' + device_name
            cu.execute("CREATE TABLE {} (\
                                            time        DOUBLE UNIQUE\
                                                               NOT NULL\
                                                               PRIMARY KEY,\
                                            temperature DOUBLE NOT NULL,\
                                            humidity    DOUBLE NOT NULL\
                                            );".format(table_name))
            return True
        except:
            return False


def delete_from_gateway(device_name, gateway):
    """
    :param device_name:设备名
    :param gateway: 网关名
    :return: None
    """
    with Connect() as cu:
        table_name = gateway + '_' + device_name
        # print("DELETE FROM {} WHERE device_name=\"{}\";".format(gateway, table_name))
        cu.execute("DELETE FROM {} WHERE device_name=\"{}\";".format(gateway, table_name))
        cu.execute("DROP TABLE {}".format(table_name))


def get_data_by_node_name(node, gateway, dtype, time_scope):
    """
    :param node: 节点名
    :param gateway:网关名
    :param dtype: 查询类型(温度或湿度)
    :param time_scope:时间范围
    :return:
    """
    table_name = gateway + '_' + node
    data = []
    time_data = []
    with Connect() as cu:
        cu.execute('select time, {} from {} where time>{}'.format(dtype, table_name, time_scope))
        fetch = cu.fetchall()
        if len(fetch):
            for item in fetch:
                time_data.append(item[0])
                data.append(item[1])
    return data, time_data


def write_data_to_gateway_node(gateway, node, data):
    """
    :param node: 节点名
    :param gateway: 网关名
    :param data: 由时间、温度、湿度组成的字典
    :return:
    """
    table_name = gateway + '_' + node
    with Connect() as cu:
        cu.execute("insert into {}(time, temperature, humidity)\
                   values({}, {}, {})".format(table_name, data['time'], data['temperature'], data['humidity']))


def get_gateway_id_by_gateway_name(gateway_name):
    with Connect() as cu:
        cu.execute("select gateway_id from gateway_info where gateway_name=\"{}\"".format(gateway_name))
        gateway_id = cu.fetchall()[0][0]
        return gateway_id


if __name__ == '__main__':
    print('Filename:datahandler.py')
    print('Function:Read data from data base or write data to data base')
