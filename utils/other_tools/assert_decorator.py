# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/4/18 10:35
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : assert_decorator.py
# ----------------------
import functools
from common.action import AppAction


def assert_log(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AssertionError as e:
            # 捕获 airtest 抛出的 AssertionError 异常，并重新定义异常信息
            error_msg = f"{func.__name__} -> {e}"
            AppAction.snapshot(is_error=True)
            raise AssertionError(error_msg)

    return wrapper
