#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2022/5/10 18:54
# @Author  : cxx
# @Email   : 1150772265@qq.com
# @File    :
# @describe:
"""

import socket


def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    _s = None
    try:
        _s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _s.connect(('8.8.8.8', 80))
        l_host = _s.getsockname()[0]
    finally:
        _s.close()

    return l_host

