#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/16/16 9:13 AM
# @Author  : YangGao
# @File    : demo.py
from configparser import ConfigParser
from push_utils import push_request_api
from push_utils.read_cfg_helper import ParameterFromConfig

server_address = ''
port = ''

'''
 request_type:
     socket_type = 1
     http_type = 2
'''
request_type = 1
msg_title = 'XunFeiPushTest'
msg_content = "this message is from xun_fei platform"

'''
 单推 或 群推 由配置cfg 文件 自行根据 device_id 判断
 这里需要处理的是 APP 推 还是 非APP推
  not_push_app = False  为 APP 推
'''
not_push_app = True

if __name__ == '__main__':
    config_file = ConfigParser()
    config_file.read('xun_fei_push.cfg')
    parameter_from_config = ParameterFromConfig(config_file)

    push_request_api.start_push(msg_title, msg_content, server_address, port, parameter_from_config, request_type,
                                not_push_app)
