# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/4/6 20:03
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : login_page.py
# ----------------------
from common.base_page import BasePage
from utils.logging_tools.log_controller import INFO
from utils.Image_processing_tools.ocr_controller import cut_text_region, recognize_text


class LoginPage(BasePage):

    def check_recommended_service(self, device, package: dict):
        device.device_conn.sleep(2)
        if device.app_action.exists(self.agree_privacy.format(package.get('name'))):
            device.app_action.touch(self.agree_privacy.format(package.get('name')))
        device.device_conn.sleep(package.get('time'))

        if device.app_action.exists(self.close_announcement.format(package.get('name'))):
            device.app_action.touch(self.close_announcement.format(package.get('name')))

            # 触碰顶部
            # width, height = device.device_conn.screen_size()
            # top_quarter = (int(width / 2), int(height / 10))
            # device.app_action.touch(top_quarter)

        device.device_conn.sleep(3)
        cut_path = device.app_action.cut_screenshot()
        cut_text_region(cut_path)
        text = recognize_text(cut_path)
        INFO.logger.info(text)
        # AssertUtil.assert_exists(self.recommended_service.format(package.get('name'), msg="推荐服"))
        # device.app_action.snapshot(99, 1200)



