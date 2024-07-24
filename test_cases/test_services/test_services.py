# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/4/7 14:45
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : test_services.py
# ----------------------
import json
import allure
import pytest
from services.login_page import LoginPage
from services.sdk_page import SDKPage
from services.cheak_adb_logs import get_adb_logs
from services.cheak_request_response import get_request_and_response, get_api_exp_ret
from utils.cache_process.cache_controller import CacheHandler
from utils.assertions.assert_type import equals

devices_list = CacheHandler.get_cache("devices_list")
package_list = CacheHandler.get_cache("package_list")


@allure.epic('EPIC: 移动端app自动化测试框架')
@allure.feature('FEATURE: 模块测试')
class TestServices:
    @allure.story('STORY: 功能测试')
    @allure.title('TITLE: 响应断言')
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('package', package_list)
    @pytest.mark.parametrize('device', devices_list)
    def test_service(self, open_close_app, package: dict):
        with allure.step("测试设备和包信息"):
            allure.attach("设备", f"{open_close_app.device_name}")
            allure.attach("包信息", f"{package.get('real_name')}")

        with allure.step("登录模块"):
            test_login_page = LoginPage()
            test_login_page.check_recommended_service(open_close_app, package)

        # with allure.step("sdk测试模块"):
        #     allure.attach("sdk step1", "打开红包悬浮球")
        #     sdk = SDKPage(open_close_app, package)
        #     sdk.open_sdk()
        #     l = sdk.get_sdk_list()
        #     allure.attach("sdk step2", f"菜单信息：{l}")

        with allure.step("日志检测模块"):
            f = get_adb_logs(package)
            for i, log_v in enumerate(f):
                allure.attach(f"日志{i}", log_v)


@allure.epic('EPIC: 移动端app自动化测试框架')
@allure.feature('FEATURE: 模块测试')
class TestResp:
    @allure.story('STORY: 响应断言')
    @allure.title('TITLE: 响应断言')
    @pytest.mark.run(order=2)
    def test_resp(self):
        ret = get_request_and_response()
        api_exp_ret = get_api_exp_ret()
        for k, v in ret.items():
            if k in api_exp_ret.keys():
                exp_ret = api_exp_ret.get(k).get('status_code')
                resp = v.get('response').get('status_code')
                equals(resp, exp_ret)

