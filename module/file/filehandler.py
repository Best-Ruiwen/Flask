import os
from module.database import datahandler


# 将数据库中的表写入CSV文件
def db2csv(username):
    tables = datahandler.get_table(username)
    for table in tables:
        os.system("sqlite3 -csv data.db \"select * from {}\" > \
                 ./download/{}/{}.csv".format(table, username, table))


# 获取文件
def get_file(username):
    download = "./download/" + username
    maps = {}
    for root, dirs, files in os.walk(download):
        for item in files:
            maps[item] = round(os.path.getsize(os.path.join(root, item))/1024, 2)  #取小数点后两位
    return maps


# 创建文件夹
def makedir(username):
    try:
        os.makedirs("./download/" + username)
        return True
    except:
        return False