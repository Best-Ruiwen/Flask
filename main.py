#!/usr/bin/python3

# 系统模块
from flask import Flask, render_template, url_for, abort
from flask import request, session, send_from_directory
import random
import os
import time
import json


# 自写模块
from module.database import datahandler as dh
from module.file import filehandler
from module.file import mail
from module.utils import rsa
from module.utils.cache import Cache
from module.apig_sdk import huawei


app = Flask(__name__)
app.secret_key = os.urandom(24)
cache = Cache()
query_time_table = (3600, 18000, 86400, 432000, 604800)  # 查询时间对照表


# 判断是否登陆
def is_login(username, status="check"):
    if session.get(username) == username:
        return True
    else:
        if status == "check":
            abort(404)
        else:
            return False


# 文件下载链接
@app.route('/download/<username>/')
def file_list(username):
    if is_login(username):
        filehandler.db2csv(username)
        maps = filehandler.get_file(username)
        if maps:
            return render_template('download.html', names=maps, id=username)

        # 没有网关或者没有设备
        return json.dumps(-1)


@app.route('/download/<username>/<filename>/')
def download(username, filename):
    if is_login(username):
        return send_from_directory(os.path.join(app.root_path, 'download/'+username), filename, as_attachment=True)


@app.route('/')
def hello():
    data, data_time = dh.get_data('node_1034')
    pie = dh.pie_handler(data)
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

    if is_login(username, status="login"):  # 判断是否已登录
        return json.dumps(0)    # 如果已经登录，则返回0

    password = request.args.get("password")
    password = rsa.decrypt(password).decode()

    result_login = dh.login(username, password)    # 验证帐号和密码 返回值：# 1代表用户名验证通过
                                                                                 # -1代表未注册的账号
                                                                                 # 0代表验证失败
                                                                                 # 其他代表返回了邮箱地址

    if result_login == 1:   # 验证成功
        session[username] = username
        return json.dumps(url_for('success', username=username))

    elif result_login == 0:  # 错误的账号密码
        return json.dumps(-1)

    elif result_login == -1:  # 未注册的账号
        return json.dumps(-1)

    else:  # 返回的是用户名
        session[result_login] = result_login
        return json.dumps(url_for('success', username=result_login))


# 登陆成功
@app.route('/user/<string:username>/')
def success(username):
    if is_login(username):
        data, data_time = dh.get_data('node_1034')
        pie = dh.pie_handler(data)
        return render_template('user_panel.html',
                               id=username,
                               data=data,
                               time=data_time,
                               pie=pie)
    else:
        return json.dumps(-1)


# 注销
@app.route('/logout/')
def logout():
    username = request.args.get('username')
    session.pop(username, None)
    return json.dumps(url_for('hello'))


# 图表(数据)界面
@app.route('/user/<username>/chart/')
def chart(username):
    # nodes = dh.get_table(username)
    if is_login(username):
        dic = dh.get_devices_by_username(username)
        return render_template("chart_panel.html",
                               gateways=dic,
                               gateway_device_dic=dic,
                               username=username)

    
# 给数据面板返回数据
@app.route('/<username>/node/', methods=['POST', 'GET'])
def node_select(username):
    if is_login(username):
        """
        node:节点名
        index：要查询的时间的下标
        gateway：网关名
        dtype：要查询的数据(温度或湿度)
        """
        node = request.args.get('node')
        index = int(request.args.get('time'))  # time字段含义：1.最近1h， 2.最近5h， 3.最近1D,  4.最近5D， 5.最近7D
        gateway = request.args.get('gateway')
        dtype = request.args.get('dtype')
        current_time = time.time()

        time_scope = current_time - query_time_table[index]
        data, time_data = dh.get_data_by_node_name(node, gateway, dtype, time_scope)  # 根据node值和时间段查询数据库
        # print(data, time_data)
        #
        pie = dh.pie_handler(data)
        ret = {'time': time_data, 'data': data, 'pie': pie}
        return json.dumps(ret)


# 控制面板
@app.route('/user/<username>/control/')
def control(username):
    if is_login(username):
        dic = dh.get_devices_by_username(username)
        return render_template("control_panel.html", id=username, gateways=dic,)


# 控制命令链接
@app.route("/user/<username>/order/")
def send_order(username):
    if is_login(username):
        gateway = request.args.get("gateway")
        node = request.args.get("node")

        # 命令代码：1.启动   0.关机  -1.立即上传数据  2.添加节点  3.删除节点
        order = request.args.get("order")
        command_status = huawei.command(gateway, node, order)
        if command_status == -1:  # 命令发送失败
            return json.dumps("操作失败，请检查设备是否在线或者网络连接是否通畅")
        return json.dumps(command_status)   # 返回设备响应结果


# 添加网关链接，网关是直连设备，连接到华为云的
@app.route("/user/<username>/add/gateway/")
def add_gateway(username):
    if is_login(username):
        gateway_name = request.args.get("gateway_name")
        gateway_id = request.args.get("gateway_id")

        # 添加到本地
        ret_add_to_local = dh.add_gateway_to_user(username, gateway_name)
        if not ret_add_to_local:
            json.dumps(-1)   # 添加到本地数据库失败，直接返回

        # 添加到华为云
        add_status = huawei.add_device(gateway_id, gateway_name)
        if add_status:  # 返回值不为空，表示注册成功了
            device_id_from_huawei = add_status[0]
            secret_from_huawei = add_status[1]

            key_secret_file_path = "./secret/" + gateway_name + '.txt'
            with open(key_secret_file_path, 'w') as f:
                f.write('gateway_id:' + device_id_from_huawei)
                f.write('\n')
                f.write('secret:' + secret_from_huawei)
            return json.dumps("/download/secret/{}/{}/".format(username, gateway_name))

        return json.dumps(1)


# 下载密钥的连接
@app.route("/download/secret/<username>/<device>/")
def download_secret(username, device):
    if is_login(username):
        return send_from_directory(os.path.join(app.root_path, 'secret'), device + ".txt", as_attachment=True)


# 添加设备，设备是属于某个网关的，设备是连接到网关的
@app.route("/user/<username>/add/device/")
def add_device(username):
    if is_login(username):
        device_name = request.args.get("device_name")
        device_id = request.args.get("device_id")
        to_gateway = request.args.get("to_gateway")
        status = dh.add_device_to_gateway(device_name=device_name,
                                          device_id=device_id,
                                          gateway=to_gateway)
        if status:  # 添加成功
            # 告知网关设备变动
            gateway_id = dh.get_gateway_id_by_gateway_name(to_gateway)
            huawei.command(gateway_id, device_name, 2)
            return json.dumps(0)
        else:   # 添加失败
            return json.dumps(1)


# 删除设备
@app.route("/user/<username>/delete/")
def delete_device(username):
    if is_login(username):
        node = request.args.get("node")
        gateway = request.args.get('gateway')
        # print(node, gateway)
        dh.delete_from_gateway(device_name=node, gateway=gateway)

        # 告知网关设备变动
        gateway_id = dh.get_gateway_id_by_gateway_name(gateway)
        huawei.command(gateway_id, node, 3)
        return json.dumps("操作成功!")


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
    if cache.get(email) == verify_code:    # 验证通过，将数据写入数据库
        username = request.args.get("username")
        username = rsa.decrypt(username).decode()
        password = request.args.get("password")
        password = rsa.decrypt(password).decode()
        if dh.register(username, password, email):
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

    if dh.isregister(email) and status == 'register':      # 邮箱已经注册，但用户在注册该邮箱
        return json.dumps(-1)

    elif (not dh.isregister(email)) and status == 'reset':  # 邮箱未注册，但用户在重置密码
        return json.dumps(-1)

    else:
        verify_code = random.randint(100000, 999999)
        # print("生成的验证码:{}".format(verify_code))
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

        if dh.resetpasswd(email, password):
            return json.dumps(0)
    return json.dumps(-1)


@app.route('/user/<username>/rectify/')
def rectify(username):
    if is_login(username):
        node = request.args.get("node")
        ip = request.args.get("ip")
        status = request.args.get("status")
        if dh.rectify(node, ip, status):
            dtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            content = "您于{}将设备\'{}\'的ip地址变更为{}，如果不是您本人操作，请尽快登录瑞文云，并修改密码。".format(dtime, node, ip)
            email = dh.getmail(username)
            mail.notify(content, email)
            return json.dumps("修改成功！")
        else:
            return json.dumps("修改失败！")


# 设备获取公钥链接
@app.route('/publickey/')
def send_key():
    return json.dumps(rsa._get_public_key())


@app.route("/huawei/upload/", methods=["POST", "GET"])
def huawei():
    data = request.data
    data = data.decode()
    if data:
        data_dict = huawei.convert_to_dic(data)
        content = data_dict["notify_data"]["body"]["content"]  # 消息内容
        gateway = data_dict["notify_data"]["header"]["node_id"]  # 网关

        for key_, val in content.items():
            val["time"] = time.time()   # 添加时间
            dh.write_data_to_gateway_node(gateway=gateway,
                                          node=key_,
                                          data=val)
    return json.dumps(0)


@app.route('/<username>/<gateway>/')
def get_devices_by_gateways(username, gateway):
    if is_login(username):
        return json.dumps(dh.get_device_by_gateway(gateway))


if __name__ == '__main__':
    file = os.listdir()
    if not ("private_key.bin" in file):
        rsa.create_rsa_key(secret_code='hahaha')
    if not ("data.db" in file):
        dh.create_database()
    if not ("download" in file):
        os.mkdir("download")
    if not ("log" in file):
        os.mkdir("log")
    if not ("secret" in file):
        os.mkdir("secret")
    app.run(port=80, host='127.0.0.1', debug=True)
