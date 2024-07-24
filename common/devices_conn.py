# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/4/4 13:51
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : devices_conn.py
# ----------------------
import time
from functools import wraps
import allure
from airtest.core.api import connect_device, sleep, start_app, stop_app, wake, clear_app, install, home, \
    uninstall, shell
from utils.logging_tools.log_controller import INFO, ERROR
from utils.other_tools.switch_conn_decorator import switch_conn


def retry(retries, delay):
    def decorator_function(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    ERROR.logger.error(
                        f"Failed to connect device! Error message: {e}")
                    attempts += 1
                    ERROR.logger.error(f"try to reconnect... ({attempts}/{retries})")
                    time.sleep(delay)
            ERROR.logger.error(f"Failed to connect device after {retries} retries!")

        return wrapper

    return decorator_function


RETRIES = 3


class DeviceConnection:
    def __init__(self, device_uuid, device_platform):
        self.device_uuid = device_uuid
        self.device_platform = device_platform
        self.conn = None
        self.connect_device()

    @allure.step(f"连接设备")
    def connect_device(self):
        for i in range(RETRIES):
            try:
                INFO.logger.info(f"Attempting to connect {self.device_uuid} for the {i + 1} times")
                if not self.conn:
                    self.conn = connect_device(f"{self.device_platform}:///{self.device_uuid}")
                    INFO.logger.info(
                        f"Device successfully connected! Platform: {self.device_platform} uuid: {self.device_uuid}")
                    break
            except Exception as e:
                ERROR.logger.error(
                    f"Failed to connect device! Error message: {e} Platform: {self.device_platform} uuid: {self.device_uuid}")
        else:
            # 重试失败，抛出异常
            raise Exception(
                f"Failed to connect device after {RETRIES} retries! Platform: {self.device_platform} uuid: {self.device_uuid}")

    # @retry(5, 5)
    # @allure.step(f"连接设备")
    # def connect_device(self):
    #     if not self.conn:
    #         INFO.logger.info(f"Attempting to connect! Platform: {self.device_platform} uuid: {self.device_uuid}")
    #         self.conn = connect_device(f"{self.device_platform}:///{self.device_uuid}")
    #         INFO.logger.info(
    #             f"Device successfully connected! Platform: {self.device_platform} uuid: {self.device_uuid}")

    @switch_conn
    def shell(self, cmd):
        if not self.conn:
            raise RuntimeError('Device not connected!')
        INFO.logger.info(f"uuid: {self.device_uuid} shell: {cmd}")
        return shell(cmd)

    @allure.step(f"打开app")
    @switch_conn
    def start_app(self, package_name, activity_name=None):
        if not self.conn:
            raise RuntimeError('Device not connected！')
        INFO.logger.info('start app: {},{}'.format(package_name, activity_name))
        start_app(package_name, activity_name)

    @allure.step(f"初始化app")
    @switch_conn
    def clear_app(self, package_name):
        if not self.conn:
            raise RuntimeError('Device not connected！')
        INFO.logger.info('clear app: {}'.format(package_name))
        clear_app(package_name)

    @allure.step(f"关闭app")
    @switch_conn
    def stop_app(self, package_name):
        if not self.conn:
            raise RuntimeError('Device not connected！')
        INFO.logger.info('stop app_action: {}'.format(package_name))
        stop_app(package_name)

    @allure.step(f"唤醒屏幕")
    @switch_conn
    def wake(self):
        """唤醒屏幕"""
        try:
            if not self.conn:
                raise RuntimeError('Device not connected！')
            INFO.logger.info('{} wake up screen'.format(self.device_uuid))
            wake()
        except Exception as e:
            ERROR.logger.error("wake up screen error, the reason is: {}".format(e))

    @switch_conn
    def home(self):
        if not self.conn:
            raise RuntimeError('Device not connected！')
        home()

    @switch_conn
    def install(self, app_path, replace=True):
        """安装app"""
        try:
            if not self.conn:
                raise RuntimeError('Device not connected！')
            INFO.logger.info('{} install {}'.format(self.device_uuid, app_path))
            install(filepath=app_path, replace=replace)
        except Exception as e:
            ERROR.logger.error("install {} error, the reason is: {}".format(app_path, e))

    @switch_conn
    def uninstall(self, package):
        """安装app"""
        try:
            if not self.conn:
                raise RuntimeError('Device not connected！')
            INFO.logger.info('{} uninstall app {}'.format(self.device_uuid, package))
            uninstall(package)
        except Exception as e:
            ERROR.logger.error("uninstall app {} error, the reason is: {}".format(package, e))

    @switch_conn
    def screen_size(self):
        orientation = self.conn.display_info['orientation']
        # 竖屏
        if orientation in [0, 2]:
            INFO.logger.info(f"当前屏幕状态：竖屏")
            width = self.conn.display_info['width']
            height = self.conn.display_info['height']
            return width, height
        # 横屏
        elif orientation in [1, 3]:
            INFO.logger.info(f"当前屏幕状态：横屏")
            height = self.conn.display_info['width']
            width = self.conn.display_info['height']
            return width, height
        else:
            ERROR.logger.error("无法获取屏幕方向信息")

    @staticmethod
    def sleep(seconds):
        """
        等待指定的秒数
        """
        INFO.logger.info(f"sleep {seconds} s")
        sleep(seconds)
