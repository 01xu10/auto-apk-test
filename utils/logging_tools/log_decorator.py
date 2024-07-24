# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/3/16 19:22
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : log_decorator.py
# ----------------------
from functools import wraps
from utils.logging_tools.log_controller import INFO, ERROR, WARNING


def log_decorator(switch: bool):
    """
    封装日志装饰器, 打印请求信息
    :param switch: 定义日志开关
    :return:
    """

    def decorator(func):
        @wraps(func)
        def swapper(*args, **kwargs):

            # 判断日志为开启状态，才打印日志
            res = func(*args, **kwargs)
            # 判断日志开关为开启状态
            if switch:
                _log_msg = f"\n======================================================\n" \
                           f"请求路径: {res.url}\n" \
                           f"请求方式: {res.method}\n" \
                           f"请求头:   {res.headers}\n" \
                           f"请求内容: {res.request_body}\n" \
                           f"接口响应内容: {res.response_data}\n" \
                           f"接口响应时长: {res.res_time} ms\n" \
                           f"Http状态码: {res.status_code}\n" \
                           "====================================================="
                # 判断正常打印的日志，控制台输出绿色
                if res.status_code == 200:
                    if res.res_time < 300:
                        INFO.logger.info(_log_msg)
                    else:
                        WARNING.logger.warning(_log_msg)
                else:
                    # 失败的用例，控制台打印红色
                    ERROR.logger.error(_log_msg)
            return res

        return swapper

    return decorator
