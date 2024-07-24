# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/4/7 11:04
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : assert_controller.py
# ----------------------
from utils.logging_tools.log_controller import ERROR, INFO
from common.setting import ensure_path_sep
from airtest.core.assertions import assert_exists
from airtest.core.api import Template
from utils.other_tools.assert_decorator import assert_log


class AssertUtil:

    @staticmethod
    @assert_log
    def assert_exists(p, msg=""):
        pos = assert_exists(Template(ensure_path_sep(p)), msg)
        INFO.logger.info(f"{msg}：{pos}")
        return pos


