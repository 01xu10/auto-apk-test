# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/4/10 15:53
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : switch_conn_decorator.py
# ----------------------

import functools
from airtest.core.api import set_current, device
from utils.logging_tools.log_controller import INFO


def switch_conn(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.conn:
            raise RuntimeError('Device not connected!')
        if device().uuid != self.device_uuid:
            set_current(self.device_uuid)
            INFO.logger.info(
                f"Set current device successfully！ Platform: {self.device_platform} uuid: {self.device_uuid}")
        return func(self, *args, **kwargs)

    return wrapper



