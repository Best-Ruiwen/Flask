from . import signer
import requests
import re
import ast
import json


key = "YOUR-HUAWEI-KEY"
secret = "YOUR-HUAWEI-SECRET"

server_url = "YOUR-HUAWEI-SERVER"
project_id = "YOUR PROJECT ID"
product_id = "YOUR PRODUCT ID"

# api列表
# 特别注意：如果body不为空，必须将其转为json，否则加密时会报错，hashlib不支持转换字典
api_list = {
    'get_devices_table': {  # 获取设备列表
        'method': 'GET',
        'url': server_url + project_id + '/devices',
        'body': ''
    },

    'add_device': {  # 添加设备
        'method': 'POST',
        'url': server_url + project_id + '/devices',
        'body': {
            "node_id": "",
            "device_name": "",
            "product_id": product_id
        }
    },

    'query_certain_device': {  # 查询某个设备的状态
        'method': 'GET',
        'url': "",
        'body': ''
    },

    'delete_device': {  # 删除设备
        'method': "DELETE",
        'url': "",
        'body': ''
    },

    'send_command': {  # 命令下发
        'method': "POST",
        'url': "",
        'body': {
            "service_id": "LightSwitch",
            "command_name": "switch",
            "paras": {
                "value": "",
                "node": ""
            }
        }
    }
}


def convert_to_dic(data):
    respond_data = re.sub('null', 'None', data)
    respond_data = re.sub('false', 'False', respond_data)
    respond_data = re.sub('true', 'True', respond_data)
    respond_data = re.sub('\"\"', 'None', respond_data)
    data_dict = ast.literal_eval(respond_data)
    return data_dict


def http_request(api):
    """
     功能：发起http请求，获取json数据，并处理后返回python字典
     参数: api:api_list中的某一项
     返回：请求响应的json，并处理为python字典
     None 主要用于删除操作
     """
    method = api['method']
    url = api['url']
    body = api['body']
    body = json.dumps(body)

    sig = signer.Signer()
    sig.Key = key
    sig.Secret = secret
    r = signer.HttpRequest(method, url)
    r.headers = {"content-type": "application/json"}
    r.body = body
    sig.Sign(r)
    resp = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body)

    respond_data = resp.content.decode()
    data_dict = {}
    if respond_data:  # 如果返回的数据不为空, 则转为字典
        data_dict = convert_to_dic(respond_data)
    return data_dict


def resolve_table(dictionary):
    """
     功能：从服务器返回的字典中，解析设备名等参数
     参数: dictionary:使用http_request得到的一个字典
     返回：{设备名:标志}字典, 和设备名列表。标志一般是设备的mac地址
     """
    device_to_id = {}
    devices = dictionary['devices']
    devices_list = []
    for item in devices:
        device_to_id[item['device_name']] = item['node_id']
        devices_list.append(item['node_id'])

    return device_to_id, devices_list
