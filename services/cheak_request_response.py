# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/7/5 9:57
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : cheak_request_response.py
# ----------------------
import json
from pprint import pprint

from common import ensure_path_sep
from utils import GetYamlData
from utils.logging_tools.log_controller import WARNING, ERROR
from utils.read_files_tools.get_all_files_path import get_matching_filenames
from utils.cache_process.cache_controller import Cache


def get_request_and_response() -> dict:
    appid = Cache("\\appid").get_cache()
    # ERROR.logger.error("appid -> {}".format(appid))
    ret_name = "".join(get_matching_filenames(ensure_path_sep("\\logs\\mitmproxy_logs\\"), appid))
    # ERROR.logger.error("ret_name -> {}".format(ret_name))
    data = GetYamlData(ensure_path_sep("\\logs\\mitmproxy_logs\\{}".format(ret_name))).get_yaml_data()
    # ERROR.logger.error("data -> {}".format(data))
    return data


def get_api_exp_ret() -> dict:
    api_exp_ret = GetYamlData(ensure_path_sep("\\resources\\api_exp_ret.yaml")).get_yaml_data()
    return api_exp_ret


if __name__ == '__main__':
    ...
    # data = get_request_and_response()
    # api_exp_ret = get_api_exp_ret()
    # print(type(api_exp_ret))
    # print(api_exp_ret)
    # # pprint(data)
    # for i, v in data.items():
    #     if i in api_exp_ret.keys():
    #         print("api_exp_ret -> {}".format(api_exp_ret.get(i).get('status_code')))
    #         # print("data -> {}".format(v.get('response').get('status_code')))
    # try:
    #     assert 1 == 1, "正确"
    #     assert 1 == 2, "错误"
    # except Exception e:
    #     1