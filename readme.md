本平台是一个基于python flask 的物联网应用平台。设备接入时，使用了华为物联网设备接入服务，详情见 https://www.huaweicloud.com/product/iothub.html 
<br>需要的 python packages:
<br>&emsp;&emsp;1. flask;
<br>&emsp;&emsp;2. pycryptodome;
<br>&emsp;&emsp;3. redis;
<br>&emsp;&emsp;4. uwsgi.
<br>需要的服务器软件:
    <br>&emsp;&emsp;1. nginx;
    <br>&emsp;&emsp;2. redis server.

用法:

    A. 在windows下:python main.py，然后在浏览器中打开 "http://127.0.0.1/"
    B. 在Ubuntu 16.04:
        1. 在终端中运行 'sudo chmod 777 configure.sh'.
        2. 在终端中运行 './configure.sh' in terminal.
        3. 启动 nginx服务器.
        4. 在终端中运行 'uwsgi uwsgi.ini'.
        5. 在浏览器中打开 "http://127.0.0.1/".

注意:
<br>&emsp;&emsp;1. 在ubuntu环境中使用时，可使用IPv6。
<br>&emsp;&emsp;2. 数据库中没有数据。
<br>&emsp;&emsp;3. 如果想尝试一下，可以直接往数据库中写入网关数据和账号数据。但由于使用了华为平台，只能在本地简单的运行，看不出效果。
<br>&emsp;&emsp;4. 如果你想将此项目用于实际环境，请注册华为云账号，然后开通华为IOT接入服务，并根据华为的教程创建产品等。然后将密钥等信息填入`moudle.apig_sdk.base.py`
中相关的位置。
<br>&emsp;&emsp;5. 如果你想实现账号注册功能，还需要搭建smtp服务器以及一个公网IP，并改动`module.file.mail.py`中的相关信息。 

