#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2022/3/28 13:22
# @Author : cxx
"""
import os
from common.setting import ensure_path_sep


def get_all_files(file_path, yaml_data_switch=False) -> list:
    """
    获取子文件路径，返回一个列表
    :param file_path: 目录路径
    :param yaml_data_switch: 是否只拿文件为 yaml格式， True为只取yaml文件
    :return:
    """
    # 创建空列表存放用例路径
    filename = []
    # 获取所有文件下的子文件名称
    for root, dirs, files in os.walk(file_path):
        for _file_path in files:
            # 拼接文件夹下所有文件路径
            path = os.path.join(root, _file_path)
            # 判断是否过滤yaml、yml文件
            if yaml_data_switch:
                if 'yaml' in path or '.yml' in path:
                    # 有用例文件，就追加到列表中
                    filename.append(path)
            else:
                # 拿改目录下所有的文件
                filename.append(path)
    return filename


def get_matching_filenames(dir, kw):
    matching_filenames = []

    # 遍历目录下的文件
    for filename in os.listdir(dir):
        # 判断文件名是否包含关键字
        if kw in filename:
            matching_filenames.append(filename)

    return matching_filenames


# if __name__ == '__main__':
#     directory = ensure_path_sep("\\logs\\adb_logcat\\")  # 替换为你要遍历的目录的路径
#     keyword = "com.jzxjz.zjcsbwx201"  # 替换为你想要的关键字
#     result = "".join(get_matching_filenames(directory, keyword))
#     print(result)
