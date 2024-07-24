# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/5/22 11:53
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : main.py.py
# ----------------------

"""对己方 API 进行抓包并记录，用于后续测试分析.
需要记录的参数有
url/method/reponse_status_code/request_time/response_time/request.content_type/requst_body/response.content_tpe/response_body
"""
from mitmproxy import tls, http

intercept_hosts = (
    "webapi.zkyouxi.com",
    "trackapi.zkyouxi.com",
    "userapi.zkyouxi.com",
    "payapi.zkyouxi.com",
    "mapi.zkyouxi.com",
    "ares.zkyouxi.com",
)
keywords = ("zkyouxi", "zkmob", "x56l.com",)


def is_ignore_host(host_name):
    if host_name in intercept_hosts:
        return False
    for kw in keywords:
        if kw in host_name:
            return False
    return True


def tls_clienthello(data: tls.ClientHelloData):
    srv = data.context.server
    server_name = srv.address or srv.peername
    if is_ignore_host(server_name[0]):
        # True: http hock 不生效; 不进行请求拦截处理，直接转发给源服务器。
        data.ignore_connection = True


def request(flow: http.HTTPFlow):
    # print(flow.id)
    header = flow.request.headers
    print(flow.request.method, flow.request.url)
    print(header.get("Content-Type", ""))
    print(flow.request.content)


def response(flow: http.HTTPFlow):
    print(flow.id)
    header = flow.response.headers
    print(flow.response.status_code)
    print(header.get("Content-Type", ""))
    print(flow.response.content)
