# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/5/25 17:41
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : mitmproxy_controller.py
# ----------------------
import json
from typing import Text, Dict
from mitmproxy import tls, http
from ruamel import yaml
from utils.cache_process.cache_controller import Cache
from utils.logging_tools.log_controller import RESP
from common.setting import ensure_path_sep
from utils.time_tools.time_control import now_time_day


class Counter:
    """
    基于 mitmproxy 库拦截获取网络请求
    参考资料: https://blog.wolfogre.com/posts/usage-of-mitmproxy/
    """

    def __init__(self, intercept_hosts: tuple, keywords: tuple, filter_url_type: list):
        self.num = 0
        self.counter = 1
        self.now_time_day = now_time_day()
        # 需要拦截的 host
        self.intercept_hosts = intercept_hosts
        # 需要拦截的 关键字
        self.keywords = keywords
        self.filter_url_type = filter_url_type
        self.url_path_list = []
        self.appid = Cache("appid").get_cache()

    def is_intercept_host(self, host_name):
        """
            判断是否拦截请求
        """
        if host_name in self.intercept_hosts:
            return True
        if any(kw in host_name for kw in self.keywords):
            return True
        return False

    def tls_clienthello(self, data: tls.ClientHelloData):
        srv = data.context.server
        server_name = srv.address or srv.peername
        if not self.is_intercept_host(server_name[0]):
            # True: http hock 不生效; 不进行请求拦截处理，直接转发给源服务器。
            data.ignore_connection = True

    def response(self, flow: http.HTTPFlow):
        # 判断过滤掉含 filter_url_type 中后缀的 url
        if any(i in flow.request.url for i in self.filter_url_type) is False:
            request_header = flow.request.headers
            RESP.logger.warning("====== Request ======")
            RESP.logger.warning("id: {}".format(flow.id))
            RESP.logger.warning("path: {}".format(flow.request.path))
            RESP.logger.warning("method: {}, url: {}".format(flow.request.method, flow.request.url))
            RESP.logger.warning("header: {}".format(request_header.get("Content-Type", "")))
            RESP.logger.warning("content: {}".format(json.loads(flow.request.text)))

            # 收集request信息
            request_data = {
                'id': flow.id,
                'method': flow.request.method,
                'url': flow.request.url,
                'request_header': flow.request.headers.get("Content-Type", ""),
                'request_content': json.loads(flow.request.text)
            }

            RESP.logger.warning("===== Response =====")
            RESP.logger.warning("status_code: {}".format(flow.response.status_code))
            response_header = flow.response.headers
            RESP.logger.warning("header: {}".format(response_header.get("Content-Type", "")))
            RESP.logger.warning("content: {}".format(flow.response.text))
            print()

            # 收集response信息
            response_data = {
                'status_code': flow.response.status_code,
                'response_header': flow.response.headers.get("Content-Type", ""),
                'response_content': json.loads(flow.response.text)
            }
            path, params = self.parse_get_request(flow.request.path)
            if path not in self.url_path_list:
                self.url_path_list.append(path)
                data = {
                    path:
                        {
                            "request": request_data,
                            "response": response_data
                        }
                }
                self.write_to_yaml(data)

    @staticmethod
    def parse_get_request(url):
        path = url.split('?')[0]  # 获取路径部分
        params = url.split('?')[1] if '?' in url else None  # 获取参数部分，如果没有参数则为None
        return path, params

    def write_to_yaml(self, data: Dict) -> None:
        """
        写入 yaml 数据
        :param data: 测试用例数据
        :return:
        """
        file_path = ensure_path_sep(
            "\\logs\\mitmproxy_logs\\http_flow_{}_{}.yaml".format(self.appid, self.now_time_day))
        with open(file_path, "a", encoding="utf-8") as file:
            yaml.dump(data, file, Dumper=yaml.RoundTripDumper, allow_unicode=True)
            file.write('\n')


intercept_host = (
    "webapi.zkyouxi.com",
    "trackapi.zkyouxi.com",
    "userapi.zkyouxi.com",
    "payapi.zkyouxi.com",
    "mapi.zkyouxi.com",
    "ares.zkyouxi.com",
)

kws = ("zkyouxi", "zkmob", "x56l.com",)

fil_url_type = ['.css', '.js', '.map', '.ico', '.png', '.woff', '.map3', '.jpeg', '.jpg']

addons = [
    Counter(intercept_host, kws, fil_url_type)
]

# 1、本机需要设置代理，默认端口为: 8080
# 2、控制台输入 mitmweb -s .\utils\recording\mitmproxy_controller.py -p 8888 --ssl-insecure --quiet
