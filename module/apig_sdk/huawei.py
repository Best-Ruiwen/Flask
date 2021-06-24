from .base import *


def get_table():
    """
    功能：从华为服务器获取设备列表
    参数: 无
    返回：{设备名:标志}字典，和设备名列表。标志一般是设备的mac地址
    """

    # 发起http请求
    dicc = http_request(api_list["get_devices_table"])

    # 解析返回的数据
    return resolve_table(dicc)


def query_certain_device_info(device_id):
    """
    功能：从华为服务器查询某个具体设备的信息
    参数: device_id:设备标志
    返回：设备状态
    """

    # 生成url
    device_id = product_id + device_id
    api_list['query_certain_device']['url'] = server_url + project_id + '/devices/' + product_id + '_' + device_id

    # 发起http请求
    dic = http_request(api_list["query_certain_device"])

    # 返回设备状态
    return dic['status']


def delete_device(device_id):
    """
    功能：从华为服务器删除设备
    参数: device_id:设备标志
    返回：True:删除成功 
    返回：False:删除失败
    """

    # 生成url
    device_id = product_id + device_id
    api_list['delete_device']['url'] = server_url + project_id + '/devices/' + product_id + '_' + device_id

    # 发起http请求
    dicc = http_request(api_list["delete_device"])

    if dicc:   # dicc 返回值不是None，表明删除失败了
        return False
    else:
        return True   # 删除成功


def add_device(device_id, device_name):
    """
    功能：添加设备到华为服务器
    参数: device_id:设备标志
    参数：device_name:设备名
    返回：device_id_from_huawei：注册成功后，华为返回的设备ID
    返回：secret：注册成功后，华为返回的secret
    返回：False：注册失败
    """

    # 构造body
    api_list['add_device']['body']['node_id'] = device_id
    api_list['add_device']['body']['device_name'] = device_name

    # 发起http请求
    dicc = http_request(api_list['add_device'])

    # 尝试从返回的数据中获取device_id和secret
    try:
        device_id_from_huawei = dicc["device_id"]
        secret_from_huawei = dicc["auth_info"]["secret"]
        ret = (device_id_from_huawei, secret_from_huawei)
        return ret
    except:  # 添加失败了，返回False
        return False


def command(device_id, node, instruction):
    """
    功能：给设备下发命令
    参数: device_id:设备标志，本项目中，指的是网关
    参数：instruction:指令指
    参数：node：实际设备
    返回：0：设备成功完成操作
    返回：1：操作失败
    返回：-1：发送命令失败/设备未响应
    """

    # 命令代码：1.启动   0.关机  -1.立即上传数据  2.添加节点  3.删除节点
    # 构造body
    api_list['send_command']['body']['paras']['value'] = instruction
    api_list['send_command']['body']['paras']['node'] = node

    # 构造url
    api_list['send_command']['url'] = server_url + project_id + '/devices/' + product_id + '_' + device_id + '/commands'
    # print(api_list['send_command']['url'])

    # 发起http请求
    dic = http_request(api_list['send_command'])

    # 获取响应结果
    try:
        status = dic['response']['paras']

        if 'switch_success' in status:
            return status['switch_success']

        else:
            return status['switch_failure']
    except:
        return -1


# if __name__ == "__main__":
    # dic, devices = get_table()
    # print(command('raventest1', 1))
