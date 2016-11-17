#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/16/16 10:05 AM
# @Author  : YangGao
# @File    : push_request_api.py

from urllib.request import urlopen, Request
import urllib.parse
import socket
import json
import _md5
from enum import Enum
import time
from push_utils import log_helper

log_helper.init_log()


class RequestType(Enum):
    socket_type = 1
    http_type = 2


conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
success_flag = False


def get_socket_connected(server_address, port):
    try:
        conn.connect((server_address, port))
        return True
    except Exception as e:
        print(e)
        log_helper.write_log(2, e)
        return False


def get_socket_connection_close():
    try:
        if conn:
            conn.close()
    except Exception as e:
        print(e)
        log_helper.write_log(2, e)


class PushHelper:
    def __init__(self):
        pass

    def push_request(self, server_address, message, request_type):

        if RequestType.socket_type.value == request_type:

            request = "POST /rest/2.0/push.do HTTP/1.1\r\nHost: %s\r\nContent-Length: %d\r\n\r\n%s" % (
                server_address, len(message), message)

            try:
                conn.send(request.encode())

                receive = conn.recv(1024 * 4)
                response_data = ''

                while len(receive > 0):
                    response_data += str(receive)
                    receive = conn.recv(1024 * 4)
                self.socket_receive_call_back(response_data)
            except Exception as e:
                print(e)
                log_helper.write_log(2, e)

        elif RequestType.http_type.value == request_type:

            url = "http://" + server_address + "/rest/2.0/push.do"
            request = Request(url, message)
            try:
                with urlopen(request) as response:
                    self.http_response_call_back(response)
            except Exception as e:
                print(e)
                log_helper.write_log(2, e)

    def http_response_call_back(self):
        pass

    def socket_receive_call_back(self):
        pass


def sign_parameter(parameter_dic, api_key, server_address):
    keys = list(parameter_dic.keys())
    keys.sort()

    sign_str = "POST%s/rest/2.0/push.do?" % server_address
    for key in keys:
        sign_str += ('{0}={1}&'.format(key, str(parameter_dic[key])))

    sign_result = str.encode(sign_str + api_key)

    return _md5.md5(sign_result).hexdigest()


def init_request_message(not_app, devices, message_title, message_content, server_address, config_info):
    real_msg = '{ "title": "%s", "content": "%s", "builder_id": 0 }' % (message_title, message_content)
    parameters = dict()
    parameters["appid"] = config_info.app_id
    parameters["push_type"] = config_info.push_type
    parameters["msg_type"] = config_info.msg_type
    parameters["click_action"] = config_info.click_action
    parameters["message"] = real_msg
    parameters["timestamp"] = int(time.time())
    parameters["expires"] = config_info.expires
    if not_app:
        if devices is not None:
            device_list = config_info.device_id.split(",")
            devices_str = ''
            for i in device_list:
                devices_str += str(i) + "\r\n"
            parameters["did"] = devices_str
        else:
            parameters["did"] = config_info.device_id

    parameters["dvc_type"] = config_info.dvc_type

    sign = sign_parameter(parameters, config_info.api_key, server_address)
    parameters["sign"] = sign
    try:
        request_message = urllib.parse.urlencode(parameters).encode("utf-8")
    except Exception as e:
        print(e)
        request_message = ''
        log_helper.write_log(2, e)
    return request_message


def parse_http_response(response):
    global success_flag
    response_data = response.read()
    data_json = json.loads(response_data)
    ret = data_json['ret']
    req_id = data_json["req_id"]
    print('this push process ret is : ', ret)
    print('this push process request id is : ', req_id)
    if ret == 0:
        log_helper.write_log(1, 'the http_push id is {} and result is : {}'.format(req_id, ret))
        success_flag = True
    else:
        log_helper.write_log(2, 'the http_push id is {} and result is : {}'.format(req_id, ret))
        success_flag = False


def parse_socket_receive_data(data):
    global success_flag
    response_data = data.split("\r\n\r\n")[1]
    data_dic = eval(response_data)
    ret = data_dic['ret']
    req_id = data_dic["req_id"]
    print('this push process ret is : ', ret)
    print('this push process request id is : ', req_id)
    if ret == 0:
        log_helper.write_log(1, 'the socket_push id is {} and result is : {}'.format(req_id, ret))
        success_flag = True
    else:
        log_helper.write_log(2, 'the socket_push id is {} and result is : {}'.format(req_id, ret))
        success_flag = False


class PushRequest(PushHelper):
    def http_response_call_back(self, response):
        if len(response) > 0:
            parse_http_response(response)

    def socket_receive_call_back(self, data):
        if len(data) > 0:
            parse_socket_receive_data(data)


def start_push(msg_title, msg_content, server_address, port, config_info, request_type, not_app):
    if request_type == 1:
        if not get_socket_connected(server_address, port):
            print('socket connect failed')
            return

    for i in range(1, config_info.push_count + 1):
        print('get start request %s - time ' % str(i))
        device_list = config_info.device_id.split(',')

        if len(device_list) > 1:
            list_push = ''
        else:
            list_push = None

        parameter_msg = init_request_message(not_app, list_push, msg_title, msg_content, server_address, config_info)

        if len(parameter_msg) > 0:
            push_requester = PushRequest()
            push_requester.push_request(server_address, parameter_msg, request_type)

        if success_flag:
            print('this %s time success' % str(i))
        else:
            print('this %s time fail' % str(i))
        time.sleep(2)
    if request_type == 1:
        get_socket_connection_close()
        print('socket closed')
