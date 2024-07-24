# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/4/14 15:29
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : clean_files.py
# ----------------------

import os
from common import ensure_path_sep


def del_file(path):
    """删除目录下的文件"""
    list_path = os.listdir(path)
    for i in list_path:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)


if __name__ == '__main__':
    del_file(ensure_path_sep("\\out_files"))
    del_file(ensure_path_sep("\\reports"))
    del_file(ensure_path_sep("\\logs"))
