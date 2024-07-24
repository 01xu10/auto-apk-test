# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/5/25 15:21
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : Observer.py
# ----------------------
import os
import subprocess
import threading
from common.setting import ensure_path_sep
from airtest.core.android.adb import ADB

from utils.logging_tools.log_controller import LogHandler
from utils.time_tools.time_control import now_time, now_time_day

f = "[adb logcat]: %(message)s"


class Observer(threading.Thread):
    def __init__(self, uuid, package):
        super(Observer, self).__init__()
        self.uuid = uuid
        self.package = package
        self.adb = ADB().adb_path
        self.stop_event = threading.Event()
        self.LOGCAT = LogHandler(ensure_path_sep("\\logs\\adb_logcat\\logcat_{}_{}.log".format(self.package.get("appid"), now_time_day())), level='debug', fmt=f)

    def run(self):

        # Start mitmweb process
        mitmweb_process = subprocess.Popen(["mitmdump", "-s", ensure_path_sep("\\utils\\recording\\mitmproxy_controller.py"), "-p", "8888", "--ssl-insecure", "--quiet"])

        # Start logcat process
        logcat_process = subprocess.Popen([self.adb, "-s", self.uuid, "logcat", f"{self.package.get('package_name')}:*"], stdout=subprocess.PIPE)

        # Continuously read logcat output
        while not self.stop_event.is_set():
            line = logcat_process.stdout.readline().decode("utf-8").strip()
            if line and self.package.get("package_name") in line:
                self.LOGCAT.logger.debug(line)

        # Stop logcat process
        logcat_process.terminate()
        logcat_process.kill()
        mitmweb_process.terminate()
        mitmweb_process.kill()

    def stop(self):
        self.stop_event.set()

