# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/3/16 19:39
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : setting.py
# ----------------------

import os
from typing import Text

"""
1.获取根路径
2.根据规则切割每个路径
3.使用os.sep根据你所处的平台，自动采用相应的分隔符号   
"""


def root_path():
    """ 获取 根路径 """
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return path


def ensure_path_sep(path: Text) -> Text:
    """兼容 windows 和 linux 不同环境的操作系统路径 """
    if "/" in path:
        path = os.sep.join(path.split("/"))

    if "\\" in path:
        path = os.sep.join(path.split("\\"))

    return root_path() + path


