# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/4/6 19:48
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : base_page.py
# ----------------------
from utils.read_files_tools.yaml_control import GetYamlData
from common.setting import ensure_path_sep


class BasePage(object):

    def __init__(self):
        self.locators = GetYamlData(file_dir=ensure_path_sep("\\resources\\all_element.yaml")).get_yaml_data()[self.__class__.__name__]
        for element_name, locator in self.locators.items():  # 遍历字典kv
            setattr(self, element_name, locator)  # 给self设置一个变量element_name的值是locator


