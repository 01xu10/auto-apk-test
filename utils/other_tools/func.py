#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  dongfanger
@Date    :  7/24/2020 5:41 PM
@Desc    :  tep函数库
"""
import copy
import inspect
import itertools
import os
import time
from sys import stdout
import yaml
from loguru import logger


def current_time():
    """
    当前时间，年-月-日 时-分-秒
    :return:
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def current_date():
    """
    当前日期 年-月-日
    :return:
    """
    return time.strftime("%Y-%m-%d", time.localtime(time.time()))


def print_progress_bar(i):
    """
    进度条
    """
    c = int(i / 10)
    progress = '\r %2d%% [%s%s]'
    a = '■' * c
    b = '□' * (10 - c)
    msg = progress % (i, a, b)
    stdout.write(msg)
    stdout.flush()


def case_pairwise(option):
    """
    pairwise算法
    """
    cp = []  # 笛卡尔积
    s = []  # 两两拆分
    for x in eval('itertools.product' + str(tuple(option))):
        cp.append(x)
        s.append([i for i in itertools.combinations(x, 2)])
    logger.info('笛卡尔积:%s' % len(cp))
    del_row = []
    print_progress_bar(0)
    s2 = copy.deepcopy(s)
    for i in range(len(s)):  # 对每行用例进行匹配
        if (i % 100) == 0 or i == len(s) - 1:
            print_progress_bar(int(100 * i / (len(s) - 1)))
        t = 0
        for j in range(len(s[i])):  # 对每行用例的两两拆分进行判断，是否出现在其他行
            flag = False
            for i2 in [x for x in range(len(s2)) if s2[x] != s[i]]:  # 找同一列
                if s[i][j] == s2[i2][j]:
                    t = t + 1
                    flag = True
                    break
            if not flag:  # 同一列没找到，不用找剩余列了
                break
        if t == len(s[i]):
            del_row.append(i)
            s2.remove(s[i])
    res = [cp[i] for i in range(len(cp)) if i not in del_row]
    logger.info('过滤后:%s' % len(res))
    return res


def load_yaml(path: str) -> dict:
    with open(path, encoding="utf8") as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)


def jwt_headers(token):
    """
    jwt请求头
    """
    return {"Content-Type": "application/json", "authorization": f"Bearer {token}"}


def data(first_node: str) -> dict:
    """
    读用例同名的yaml文件
    取首节点的值
    """
    caller = inspect.stack()[1]
    case_path = os.path.dirname(caller.filename)
    basename = os.path.basename(caller.filename)
    data_path_yml = os.path.join(case_path, basename.rstrip(".py") + ".yml")
    data_path_yaml = os.path.join(case_path, basename.rstrip(".py") + ".yaml")
    node_value = {}
    if not os.path.exists(data_path_yml) and not os.path.exists(data_path_yaml):
        logger.error("数据文件不存在")
        return node_value
    data_path = data_path_yml if os.path.exists(data_path_yml) else data_path_yaml
    try:
        return load_yaml(data_path)[first_node]
    except KeyError:
        logger.error(f"数据文件{data_path}不存在首节点{first_node}")
