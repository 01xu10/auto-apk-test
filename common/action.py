# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/3/17 15:51
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : action.py
# ----------------------
import allure
from PIL import Image
from airtest.aircv import crop_image, aircv
from airtest.core.api import snapshot, touch, text, Template, exists, double_click, swipe, keyevent
from airtest.core.helper import G
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from common.devices_conn import DeviceConnection
from utils.logging_tools.log_controller import INFO, ERROR, WARNING
from common.setting import ensure_path_sep
from utils.other_tools.switch_conn_decorator import switch_conn
from utils.time_tools.time_control import now_time


class AppAction:
    def __init__(self, device_connection: DeviceConnection):
        self.conn = device_connection.conn
        self.device = device_connection
        self.device_uuid = device_connection.device_uuid

    @allure.step("元素点击")
    @switch_conn
    def touch(self, p):
        """触摸屏幕"""
        try:
            if isinstance(p, str):
                touch(Template(ensure_path_sep(p)))
            elif isinstance(p, tuple):
                touch(p)
            INFO.logger.info('touch {}'.format(p))
        except Exception as e:
            ERROR.logger.error("touch {} error, the reason is: {}".format(p, e))
            with allure.step("touch error"):
                allure.attach(str(e), "touch {} error".format(p), allure.attachment_type.TEXT)
            self.snapshot(is_error=True)

    @allure.step("查询元素")
    @switch_conn
    def exists(self, p):
        """查询元素是否存在"""
        INFO.logger.info('exists {}'.format(p))
        return exists(Template(ensure_path_sep(p)))

    @switch_conn
    def input_text(self, content):
        """触摸屏幕"""
        try:
            text(content)
            INFO.logger.info('input context: {}'.format(content))
        except Exception as e:
            ERROR.logger.error("input context {} error, the reason is: {}".format(content, e))
            self.snapshot(is_error=True)

    @switch_conn
    def double_click(self, p):
        """触摸屏幕"""
        try:
            double_click(Template(ensure_path_sep(p)))
            INFO.logger.info('double_click {}'.format(p))
        except Exception as e:
            ERROR.logger.error("double_click {} error, the reason is: {}".format(p, e))
            self.snapshot(is_error=True)

    @switch_conn
    def swipe(self, v1, v2=None, vector=None, **kwargs):
        """滑动"""
        try:
            swipe(v1, v2=v2, vector=vector, **kwargs)
            INFO.logger.info('swipe {} to {}'.format(v1, v2))
        except Exception as e:
            ERROR.logger.error("swipe {} to {} error, the reason is: {}".format(v1, v2, e))
            self.snapshot(is_error=True)

    @switch_conn
    def key_event(self, key):
        """key_event"""
        try:
            keyevent(key)
            INFO.logger.info('key: {}'.format(key))
        except Exception as e:
            ERROR.logger.error("key: {} error, the reason is: {}".format(key, e))
            self.snapshot(is_error=True)

    @staticmethod
    def snapshot(quality=99, max_size=1920, is_error=False):
        """截图"""
        path_prefix = "\\out_files\\snapshot\\"
        prefix = "normal"
        if is_error:
            prefix = "error"
        file_path = ensure_path_sep("{}{}\\{}.png".format(path_prefix, prefix, now_time))
        snapshot(filename=file_path, quality=quality, max_size=max_size)
        INFO.logger.info('snapshot -> {}'.format(file_path))
        with open(file_path, "rb") as f:
            file_content = f.read()
        allure.attach(file_content, name="Screenshot", attachment_type=allure.attachment_type.PNG)
        return file_content

    @allure.step("裁剪截图")
    def cut_screenshot(self):
        """
        对屏幕截图进行裁剪
        Returns:
            save_path: 裁剪后保存的图片
        """
        # 获取屏幕截图
        screenshot = G.DEVICE.snapshot(quality=99)
        # 获取屏幕尺寸
        orientation = self.conn.display_info['orientation']
        # WARNING.logger.warning(orientation)
        scaling = self.get_scaling(orientation)
        width, height = self.device.screen_size()
        # WARNING.logger.warning(self.conn.screen_size())
        # 计算矩形区域的实际像素坐标
        region_top, region_bottom, region_left, region_right = scaling
        rect = [
            int(region_left * width),
            int(region_top * height),
            int(region_right * width),
            int(region_bottom * height)
        ]
        # 对需要截取的区域进行裁剪并保存
        # cropped_screenshot_array = crop_image(screenshot, rect)
        crop_photo = aircv.crop_image(screenshot, rect)
        # cropped_screenshot = Image.fromarray(cropped_screenshot_array)
        save_path = ensure_path_sep('\\out_files\\snapshot\\cut\\{}.png'.format(now_time()))
        INFO.logger.info(save_path)
        aircv.imwrite(save_path, crop_photo, 99)
        # cropped_screenshot.save(save_path)
        with open(save_path, "rb") as f:
            file_content = f.read()
        allure.attach(file_content, name="cutScreenshot", attachment_type=allure.attachment_type.PNG)
        return save_path

    @staticmethod
    def get_scaling(orientation):
        scaling = [0.71, 0.8, 0.3, 0.65]
        if orientation in [1, 3]:
            scaling = [0.56, 0.73, 0.38, 0.59]
        INFO.logger.info(scaling)
        return scaling


class PocoUIAuto:
    def __init__(self, device):
        self.poco = AndroidUiautomationPoco(device=device, use_airtest_input=True, screenshot_each_action=False)

