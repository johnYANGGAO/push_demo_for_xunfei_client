#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/16/16 10:05 AM
# @Author  : YangGao
# @File    : log_helper.py

import time
import socket
import logging

base_name = 'PushLog'
local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
local_ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))


def init_log():
    log_name = base_name + ".out"

    logging.basicConfig(filename=log_name,
                        level=logging.DEBUG
                        )


def write_log(log_type, content):
    log_content = ' \n' + local_time + '/' + local_ip + ':\n' + content
    if log_type == 1:
        logging.info(log_content)
    elif log_type == 2:
        logging.error(log_content)
    elif log_type == 3:
        logging.debug(log_content)
    else:
        logging.info(log_content)

#
# def write_log_to_file(file_name, result_list):
#     result_line = ""
#
#     if not os.path.exists(file_name):
#         file = open(file_name, 'w')
#     else:
#         file = open(file_name, 'a')
#
#     for result in result_list:
#         if result_line == "":
#             result_line += result
#         else:
#             result_line += "\n" + result
#
#     file.write("%s\n" % result_line)
#     file.close()
