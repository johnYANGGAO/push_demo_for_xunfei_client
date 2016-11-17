#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/16/16 10:09 AM
# @Author  : leiyuan , YangGao
# @File    : read_cfg_helper.py


import sys
import getopt


class ParameterFromConfig:
    def __init__(self, config_file):
        self.push_num = 'default'
        self.msg_size = 'default'
        self.app_id = 'default'
        self.api_key = 'default'
        self.device_id = "default"
        self.expires = "default"
        self.click_action = "default"

        self.push_type = "default"
        self.msg_type = "default"
        self.dvc_type = "default"
        # self.conf = config_file
        self.read_config_param(config_file)
        self.get_parameter()

    # 读取配置文件：读取配置文件配置的参数
    def read_config_param(self, conf):
        try:
            self.push_num = conf.get('common', 'push_num')
            if self.push_num == '':
                self.push_num == 'default'
        except:
            self.push_num = 'default'

        try:
            self.msg_size = conf.get('common', 'msg_size')
            if self.msg_size == '':
                self.msg_size == 'default'
        except:
            self.msg_size = 'default'

        try:
            self.app_id = conf.get('common', 'app_id')
            if self.app_id == '':
                self.app_id == 'default'
        except:
            self.app_id = 'default'

        try:
            self.api_key = conf.get('common', 'api_key')
            if self.api_key == '':
                self.api_key == 'default'
        except:
            self.api_key = 'default'

        try:
            self.device_id = conf.get('common', 'device_id')
            if self.device_id == '':
                self.device_id == 'default'
        except:
            self.device_id = 'default'

        try:
            self.click_action = conf.get('common', 'click_action')
            if self.click_action == '':
                self.click_action == 'default'
        except:
            self.click_action = 'default'

        try:
            self.expires = conf.get('common', 'expires')
            if self.expires == '':
                self.expires == 'default'
        except:
            self.expires = 'default'

        try:
            self.push_type = conf.get('choose', 'push_type')
            if self.push_type == '':
                self.push_type == 'default'
        except:
            self.push_type = 'default'

        try:
            self.msg_type = conf.get('choose', 'msg_type')
            if self.msg_type == '':
                self.msg_type == 'default'
        except:
            self.msg_type = 'default'

        try:
            self.dvc_type = conf.get('choose', 'dvc_type')
            if self.dvc_type == '':
                self.dvc_type == 'default'
        except:
            self.dvc_type = 'default'

    # 读取命令行：读取命令行参数
    def get_parameter(self):
        opts, args = getopt.getopt(sys.argv[1:], "hv:",
                                   ["help=", "version=", "pn=", "ms=", "appid=", "ak=", "did=", "expires=", "ca=",
                                    "pt=", "mt=", "dt="])
        for op, value in opts:
            if op == "--pn":
                self.push_num = value
            elif op == "--ms":
                self.msg_size = value
            elif op == "--pid":
                self.app_id = value
            elif op == "--ak":
                self.api_key = value
            elif op == "--did":
                self.device_id = value
            elif op == "--expires":
                self.expires = value
            elif op == "--ca":
                self.click_action = value
            elif op == "--pt":
                self.push_type = value
            elif op == "--mt":
                self.msg_type = value
            elif op == "--dt":
                self.dvc_type = value
            elif op in ("-h", "--help"):
                usage()
            elif op in ("-v", "--version"):
                push_version()
        return True


# 提示：提示使用方法
def usage():
    print("选项\t含义\t默认值")

    print("-h or --help\t帮助\t只显示命令行参数含义，不执行脚本，退出")

    print("-v or --version\t此python推送样例版本号，不执行脚本，退出")

    print("--pn\t推送的次数\tdefault")

    print("--ms\t推送消息的大小\tdefault")

    print("--pid\tApp ID\tdefault")

    print("--ak\tApi Key\tdefault")

    print("--did\tdevice_id\tdefault")

    print("--expires\tExpires\tdefault")

    print("--ca\tClick Action\tdefault")

    print("--pt\t推送的类型\tdefault")

    print("--mt\t消息的类型\tdefault")

    print("--dt\t设备的类型\tdefault")
    sys.exit(0)


# 版本号：显示此python推送样例版本号
def push_version():
    print('PushPythonSample.py 1.1')
    sys.exit(0)
