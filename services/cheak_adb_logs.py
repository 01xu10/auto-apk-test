# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/7/5 9:56
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : cheak_adb_logs.py
# ----------------------
from common.setting import ensure_path_sep
from utils.read_files_tools.get_all_files_path import get_matching_filenames
from utils.logging_tools.log_controller import WARNING


def get_adb_logs(package):
    err_logs = []
    log_name = "".join(get_matching_filenames(ensure_path_sep("\\logs\\adb_logcat\\"), package.get('appid')))
    WARNING.logger.warning(log_name)
    with open(ensure_path_sep("\\logs\\adb_logcat\\{}".format(log_name)), "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if " E " in line:
                err_logs.append(line)
    return err_logs
