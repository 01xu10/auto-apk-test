# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/7/5 9:55
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : sdk_page.py
# ----------------------
import time

from common.base_page import BasePage
from common.device import AndroidDevice
from utils.logging_tools.log_controller import WARNING, INFO, ERROR


class SDKPage(BasePage):
    def __init__(self, device: AndroidDevice, package):
        super().__init__()
        self.poco = device.poco_obj.poco
        self.package = package

    def open_sdk(self):
        try:
            INFO.logger.info("sleep 3 s")
            time.sleep(3)
            self.poco(self.sdk_image_icon.format(self.package.get('package_name'))).click()
            INFO.logger.info("sleep 8 s")
            time.sleep(12)
        except Exception as e:
            ERROR.logger.error(f"悬浮球打开失败：{e}")

    def get_sdk_list(self):
        try:
            menu_list = []
            menu_node = self.poco("_main").child("android.view.View").child("android.widget.TextView")
            for menu in menu_node:
                menu_list.append(menu.get_text())
            return menu_list
        except Exception as e:
            ERROR.logger.error(f"菜单列表获取失败：{e}")