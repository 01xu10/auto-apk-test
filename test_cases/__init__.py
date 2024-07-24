# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/4/8 23:20
# @Author : xu
# @File : __init__.py.py
# ----------------------
import os
from common import ensure_path_sep
from common.device import DeviceFactory
from utils.apk_tools.apk_control import ApkUtils
from utils.logging_tools.log_controller import INFO
from utils.cache_process.cache_controller import CacheHandler, Cache
from utils.read_files_tools.get_all_files_path import get_all_files
from utils.read_files_tools.yaml_control import GetYamlData

devices_info = GetYamlData(ensure_path_sep("\\resources\\mobile_device_info.yaml")).get_yaml_data()


def devices_connect_init():
    """
    设备连接
    """
    for d, v in devices_info.items():
        conn = DeviceFactory.get_connection(v.get("uuid"), v.get("platform"), d)
        CacheHandler.add_to_cache_list(cache_name="devices_list", value=conn)
    INFO.logger.info("=========设备集群初始化完毕=========")


def package_init():
    """
    初始化包
    """
    apk_list = get_all_files(ensure_path_sep("\\resources\\apk\\"))
    CacheHandler.update_cache(cache_name="apk_list", value=apk_list)
    for apk in apk_list:
        package_dict = {}
        a = ApkUtils(apk)
        real_name = os.path.basename(apk).split('.')[0]
        name = real_name.split('_')[0]
        package_dict["name"] = name
        package_dict["real_name"] = real_name
        package_dict["time"] = 40 if name == "我在江湖" else 20
        package_dict["package_name"] = a.get_package_name()
        package_dict["path"] = apk
        package_dict["appid"] = a.get_meta_data("ZK_AGNET_APPID")
        Cache("appid").set_caches(a.get_meta_data("ZK_AGNET_APPID"))
        permissions = a.get_manual_high_permissions()
        CacheHandler.add_to_cache_list(cache_name="package_list", value=package_dict)
        CacheHandler.update_cache(cache_name="permissions_{}".format(a.get_package_name()), value=permissions)


package_init()
devices_connect_init()

