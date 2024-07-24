# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/4/8 23:21
# @Author : xu
# @File : conftest.py
# ----------------------
import pytest
from common import ensure_path_sep
from common.device import AndroidDevice
from utils.logging_tools.Observer import Observer
from utils.logging_tools.log_controller import INFO, RESP
from utils.read_files_tools.clean_files import del_file


@pytest.fixture(scope="session", autouse=True)
def begin():
    print()
    INFO.logger.info("=======测试开始=======")
    yield
    INFO.logger.info("=======测试结束=======")


@pytest.fixture(scope='function')
def open_close_app(device: AndroidDevice, package: dict):
    # 获取设备屏幕信息
    device.device_conn.sleep(2)
    device.device_conn.wake()
    if device.device_name in ["redmi_note8"]:
        width, height = device.device_conn.screen_size()
        bottom_quarter = (int(width / 2), int(3 * height / 4))
        top_quarter = (int(width / 2), int(height / 4))
        device.app_action.swipe(v1=bottom_quarter, v2=top_quarter)

    # device.device_conn.clear_app(package.get("package_name"))
    device.device_conn.start_app(package.get("package_name"))
    device.set_permission(package.get("package_name"))
    # 启动接口，日志拦截
    observer = Observer(device.device_uuid, package)
    observer.start()
    RESP.logger.warning("开启观察者模式")

    yield device

    observer.stop()
    observer.join()
    RESP.logger.warning("已关闭观察者模式")
    print()
    device.device_conn.stop_app(package.get("package_name"))


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的 item 的 name 和 node_id 的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")

    # 期望用例顺序
    # print("收集到的测试用例:%s" % items)
    appoint_items = ["test_services", "test_resp"]

    # 指定运行顺序
    run_items = []
    for i in appoint_items:
        for item in items:
            module_item = item.name.split("[")[0]
            if i == module_item:
                run_items.append(item)

    for i in run_items:
        run_index = run_items.index(i)
        items_index = items.index(i)

        if run_index != items_index:
            n_data = items[run_index]
            run_index = items.index(n_data)
            items[items_index], items[run_index] = items[run_index], items[items_index]


@pytest.fixture(scope="session", autouse=True)
def clear_report():
    """如clean命令无法删除报告，手动删除"""
    del_file(ensure_path_sep("\\reports\\allure_reports"))


@pytest.mark.optionalhook
def pytest_html_results_table_html(report, data):
    """Called after building results table additional HTML."""
    report.nodeid.encode("unicode_escape").decode("utf-8")


"""安装，删除apk（游戏资源太大，弃用）"""
# @pytest.fixture(scope="session", autouse=True)
# def install_and_uninstall_app():
#     """
#     安装apk fixture
#     """
#     for d in devices_list:
#         for p in CacheHandler.get_cache("apk_list"):
#             d.device_conn.install(p, replace=True)
#             INFO.logger.info("{} install {} success".format(d.device_name, p))
#
#     yield
#
#     for d in devices_list:
#         for p in package_list:
#             d.device_conn.uninstall(p.get('package_name'))
#             INFO.logger.info("{} uninstall {} success".format(d.device_name, p.get('name')))
