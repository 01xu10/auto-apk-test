# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/7/14 11:04
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : test1.py
# ----------------------
from utils.apk_tools.apk_control import ApkUtils
from common.setting import ensure_path_sep
path = r'C:\Users\Administrator\Downloads\test4.apk'
a = ApkUtils(path)
# print(a.get_manifest())
print(a.get_manifest())

