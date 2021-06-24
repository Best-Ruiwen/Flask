import os
from module.database import datahandler as dh


# 将数据库中的表写入CSV文件
def db2csv(username):
    tables = dh.get_devices_by_username(username)
    # 有网关
    if tables:
        device_tables = []
        for gateway, device in tables.items():
            # 有设备
            if device:
                for item in device:
                    device_tables.append(gateway + "_" + item)

        if device_tables:
            for table in device_tables:
                os.system("sqlite3 -header -csv data.db \"select * from {}\" > \
                         ./download/{}/{}.csv".format(table, username, table))

            return True

    # 没有网关或没有设备
    return False


# 获取文件
def get_file(username):
    """
    :param username:
    :return: {文件名：大小组成的字典}
    """
    download = "./download/" + username
    maps = {}
    for root, dirs, files in os.walk(download):
        for item in files:
            maps[item] = round(os.path.getsize(os.path.join(root, item))/1024, 2)  #取小数点后两位
    return maps


# 创建文件夹
def makedir(username):
    try:
        os.mkdir("./download/" + username)
        return True
    except:
        return False