import sqlite3
from module.database import base


def ttt():
    try:
        with base.Connect() as cu:
            cu.execute("select password from userinfo where username = \'{}\'".format('sdfsdfs'))
            cu_ret = cu.fetchall()
            # print(bool(len(cu_ret)))
            print(cu_ret[0][0])
            return True
    except:
        return False

# cx = sqlite3.connect('data.db')
# cu = cx.cursor()
#
# cu.execute("update userinfo set password=\"{}\" where email=\"{}\"".format('password', 'email'))
# cx.commit()
# cu.close()
# cx.close()


print(ttt())
# print(bool(2))
