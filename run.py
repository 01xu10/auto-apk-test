# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/4/7 17:10
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : run.py
# ----------------------
import os
import pytest
from common.setting import ensure_path_sep
from utils.notify.lark import FeiShuTalkChatBot
from utils.other_tools.allure_data.get_allure_data import AllureFileClean
from utils.other_tools.model import NotificationType
from utils import config

if __name__ == '__main__':

    pytest.main(['-s', '-W', 'ignore:Module already imported:pytest.PytestWarning',
                 '--alluredir={}'.format(ensure_path_sep("\\reports\\allure_reports")),
                 # '--html={}'.format(ensure_path_sep("\\reports\\html_reports\\html_report_{}.html".format(now_time()))),
                 # '--capture=sys', '--clean-alluredir'
                 # "-n", "2", "--dist=loadscope",
                 ])
    os.system('allure generate ./reports/allure_reports -o ./reports/allure_reports/html --clean')
    """统计用例数量"""
    allure_data = AllureFileClean.get_case_count()
    notification_mapping = {
        NotificationType.FEI_SHU.value: FeiShuTalkChatBot(allure_data).post
    }
    # 判断是否发送通知
    if config.notification_type != NotificationType.DEFAULT.value:
        notification_mapping.get(config.notification_type)()

    os.system('allure serve --port {} ./reports/allure_reports'.format(config.allure_port))
