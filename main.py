#!/usr/bin/python3

# 系统模块
from flask import Flask, render_template, url_for
from flask import request, session, send_from_directory
import random
import os
import time
import json
import socket


# 自写模块
from module.database import datahandler
from module.file import filehandler
from module.file import mail
from module.utils import rsa
from module.utils.cache import Cache


app = Flask(__name__)
app.secret_key = os.urandom(24)
cache = Cache()
query_time_table = (3600, 18000, 86400, 432000, 604800)  # 查询时间对照表


# 判断是否登陆
def islogin(username):
    if session.get(username) == username:
        return True
    return False


# 文件下载链接
@app.route('/download/<username>/')
def filelist(username):
    if islogin(username):
        filehandler.db2csv(username)
        maps = filehandler.get_file(username)
        return render_template('download.html', names=maps, id=username)
    return json.dumps(-1)


@app.route('/download/<username>/<filename>/')
def download(username, filename):
    if islogin(username):
        return send_from_directory(os.path.join(app.root_path,'download/'+username), filename, as_attachment=True)
    return json.dumps(-1)


@app.route('/')
def hello():
    data, data_time= datahandler.get_data('node_1034')
    pie = datahandler.pie_handler(data)
    return render_template('index.html', data=data, time=data_time, pie=pie)


# 登陆界面
@app.route('/login/')
def login():
    return render_template('login.html', public_key=rsa.get_public_key())


# 登陆提交链接
@app.route('/submit/', methods=['POST', 'GET'])
def login_submit():
    username = request.args.get("username")
    username = rsa.decrypt(username).decode()

    if islogin(username):  # 判断是否已登录
        return json.dumps(0)    # 如果已经登录，则返回0

    password = request.args.get("password")
    password = rsa.decrypt(password).decode()

    result_login = datahandler.login(username, password)    # 验证帐号和密码 返回值：# 1代表用户名验证通过
                                                                                 # -1代表未注册的账号
                                                                                 # 0代表验证失败
                                                                                 # 其他代表返回了邮箱地址

    if result_login == 1:   # 验证成功
        session[username] = username
        return json.dumps(url_for('success', username=username))
        # return json.dumps("http://localhost/user/{}/".format(username))

    elif result_login == 0:  # 错误的账号密码
        return json.dumps(-1)

    elif result_login == -1:  # 未注册的账号
        return json.dumps(-1)

    else:  # 返回的是用户名
        session[result_login] = result_login
        return json.dumps(url_for('success', username=result_login))
        # return json.dumps("http://localhost/user/{}/".format(result_login))


# 登陆成功
@app.route('/user/<string:username>/')
def success(username):
    if islogin(username):
        data, data_time = datahandler.get_data('node_1034')
        pie = datahandler.pie_handler(data)
        return render_template('user_panel.html', id=username, users=datahandler.get_table(username),
                               data=data, time=data_time, pie=pie)
    else:
        return json.dumps(-1)


# 注销
@app.route('/logout/')
def logout():
    username = request.args.get('username')
    session.pop(username, None)
    # return json.dumps("http://localhost/index/")
    return json.dumps(url_for('hello'))


# 图表(数据)界面
@app.route('/user/<username>/chart/')
def chart(username):
    nodes = datahandler.get_table(username)
    if islogin(username):
        return render_template("chart_panel.html", nodes=nodes, id=username)
    return json.dumps(-1)

    
# 数据面板中改变节点
@app.route('/<username>/node/', methods=['POST', 'GET'])
def node_select(username):
    if islogin(username):
        node = request.args.get('node')
        index = int(request.args.get('time')) - 1  # time字段含义：1.最近1h， 2.最近5h， 3.最近1D,  4.最近5D， 5.最近7D
        current_time = time.time()

        query_time = current_time - query_time_table[index]
        data, time_data = datahandler.get_data(node, query_time)  # 根据node值和时间段查询数据库
        print(data, time_data)

        pie = datahandler.pie_handler(data)
        ret = {'time': time_data, 'data': data, 'pie': pie}
        return json.dumps(ret)
    return json.dumps(-1)


# 控制面板
@app.route('/user/<username>/control/')
def control(username):
    # print(datahandler.get_table(username))
    tables = datahandler.get_table(username)
    if islogin(username):
        return render_template("control_panel.html", tables=tables, id=username)
    return json.dumps(-1)


# 控制命令链接
@app.route("/user/<username>/order/")
def send_order(username):
    if islogin(username):
        node = request.args.get("node")
        order = request.args.get("order")  # 命令代码：1.启动   0.关机  -1.立即上传数据
        remote, status= datahandler.getipBydeviceName(node)
        print("节点:{}, 命令:{}".format(node, order))
        addr = (remote, 10086)
        try:
            if status == "4":
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            else:
                s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
                
            msg = (node + ',' + str(order))
            s.sendto(msg.encode('utf-8'), addr)
            return json.dumps("1")
        except:
            return json.dumps(-1)
    return json.dumps(-1)


# 添加设备链接
@app.route("/user/<username>/adddevice/")
def add_device(username):
    if islogin(username):
        node = request.args.get("node")
        ip = request.args.get("ip")
        status = request.args.get("status")
        ret = datahandler.add_device(node, username, ip, status)
        if ret == "添加成功":
            dtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            content = "您于{}添加了设备\'{}\'，该设备\ip地址为{}，如果不是您本人操作，请尽快登录瑞文云，并修改密码。".format(dtime, node, ip)
            email = datahandler.getmail(username)
            mail.notify(content, email)
            return json.dumps("success")
        # return json.dumps(datahandler.add_device(username, node))
    return json.dumps(-1)


# 删除设备
@app.route("/user/<username>/delete/")
def delete_device(username):
    if islogin(username):
        node = request.args.get("node")
        datahandler.delete_device(username, node)
        return json.dumps("操作成功!")
    return json.dumps(-1)


# 注册页
@app.route('/register/')
def register():
    return render_template("register.html", public_key=rsa.get_public_key())


# 注册，提交用户名和密码
@app.route("/register/submit/", methods=["POST", "GET"])
def register_submit():
    email = request.args.get("email")
    email = rsa.decrypt(email).decode()
    verify_code = request.args.get("verify_code")
    print("收到的验证码:{}".format(verify_code))
    if cache.get(email) == verify_code:    # 验证通过，将数据写入数据库
        print("验证通过!")
        username = request.args.get("username")
        username = rsa.decrypt(username).decode()
        password = request.args.get("password")
        password = rsa.decrypt(password).decode()
        if datahandler.register(username, password, email):  
            session[username] = username   # 如果注册成功，则自动登录
            filehandler.makedir(username)  # 创建文件夹
            return json.dumps("/user/{}/".format(username))
        return json.dumps(-1)

    return json.dumps(0)


# 获取验证码链接
@app.route('/register/verify/', methods=["POST", "GET"])
def verify():
    email = request.args.get("email")
    email = rsa.decrypt(email).decode()

    status = request.args.get("status")      # register，或者reset

    if datahandler.isregister(email) and status == 'register':      # 邮箱已经注册，但用户在注册该邮箱
        return json.dumps(-1)

    elif (not datahandler.isregister(email)) and status == 'reset':  # 邮箱未注册，但用户在重置密码
        return json.dumps(-1)

    else:
        verify_code = random.randint(100000, 999999)
        print("生成的验证码:{}".format(verify_code))
        cache.set(email, verify_code)
        mail.sendmail(email, verify_code)
    return json.dumps(0)


# 重置密码
@app.route('/resetpasswd/')
def reset():
    return render_template("resetpasswd.html", public_key=rsa.get_public_key())


# 重置密码提交数据连接
@app.route('/resetpasswd/submit/')
def reset_verify():
    email = request.args.get("email")
    email = rsa.decrypt(email).decode()
    verify_code = request.args.get("verify_code")
    if cache.get(email) == verify_code:    # 验证通过，将数据写入数据库
        password = request.args.get("password")
        password = rsa.decrypt(password).decode()

        if datahandler.resetpasswd(email, password):
            return json.dumps(0)
    return json.dumps(-1)


@app.route('/user/<username>/rectify/')
def rectify(username):
    if islogin(username):
        node = request.args.get("node")
        ip = request.args.get("ip")
        status = request.args.get("status")
        if datahandler.rectify(node, ip, status):
            dtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            content = "您于{}将设备\'{}\'的ip地址变更为{}，如果不是您本人操作，请尽快登录瑞文云，并修改密码。".format(dtime, node, ip)
            email = datahandler.getmail(username)
            mail.notify(content, email)
            return json.dumps("修改成功！")
        else:
            return json.dumps("修改失败！")
    return json.dumps(-1)


# 设备获取公钥链接
@app.route('/publickey/')
def send_key():
    return json.dumps(rsa._get_public_key())


# 数据上传链接
@app.route('/upload/<device>/', methods=["POST", "GET"])
def upload(device):
    # 判断用户名和密码
    try:
        username = request.form['username']
        passwd = request.form['password']
        
        username = rsa.decrypt_upload_data(username).decode()
        passwd = rsa.decrypt_upload_data(passwd).decode()
    except:
        return json.dumps('Type error')
        
    if datahandler.login(username, passwd) == 1:
        # 判断设备是否注册
        if datahandler.isregister_device(device): # 已经注册过的设备
            data = request.form['data']
            data = float(rsa.decrypt_upload_data(data).decode())
            print(data)
            current_time = time.time()
            datahandler.write_data(device, current_time, data)
            return json.dumps(0)
        return json.dumps(-1)  # 未注册的设备

    return json.dumps(-2)  # 用户名或者密码错误


if __name__ == '__main__':
    file = os.listdir()
    if not ("private_key.bin" in file):
        rsa.create_rsa_key(secret_code='rivenriven')
    if not ("data.db" in file):
        datahandler.create_database()
    if not ("download" in file):
        os.mkdir("download")
    if not ("log" in file):
        os.mkdir("log")
    app.run(port=80, host='127.0.0.1', debug=True)
