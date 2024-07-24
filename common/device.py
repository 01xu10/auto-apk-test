# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/4/5 15:57
# @Author : xu
# @File : device.py
# ----------------------
from common.devices_conn import DeviceConnection
from common.action import AppAction, PocoUIAuto
from utils.cache_process.cache_controller import CacheHandler
from utils.logging_tools.log_controller import INFO


class AndroidDevice:
    def __init__(self, device_uuid, device_platform, device_name=None):
        self.device_conn = DeviceConnection(device_uuid, device_platform)
        self.app_action = AppAction(self.device_conn)
        self.poco_obj = PocoUIAuto(self.device_conn.conn)
        self.device_name = device_name
        self.device_uuid = device_uuid

    def set_permission(self, package_name):
        permissions = CacheHandler.get_cache(f"permissions_{package_name}")
        for permission_name in permissions:
            self.device_conn.shell(f"pm grant {package_name} {permission_name}")

        # 写入外部存储器的权限
        # self.device_conn.shell(f"pm grant {package_name} android.permission.WRITE_EXTERNAL_STORAGE")
        # 读取外部存储器的权限
        # self.device_conn.shell(f"pm grant {package_name} android.permission.READ_EXTERNAL_STORAGE")
        # 获取位置信息
        # self.device_conn.shell(f"pm grant {package_name} android.permission.ACCESS_COARSE_LOCATION")
        # self.device_conn.shell(f"pm grant {package_name} android.permission.ACCESS_FINE_LOCATION")
        # 访问媒体库的权限
        # self.device_conn.shell(f"pm grant {package_name} android.permission.MEDIA_CONTENT_CONTROL")


class IOSDevice:
    def __init__(self, device_uuid, device_platform, device_name=None):
        self.device_conn = DeviceConnection(device_uuid, device_platform)
        self.app_action = AppAction(self.device_conn)
        self.device_name = device_name


class DeviceFactory:
    connections = {}

    @classmethod
    def get_connection(cls, device_uuid, device_platform, device_name=None):
        INFO.logger.info(f"\nIncoming device information \n"
                         f"platform: {device_platform} \n"
                         f"name: {device_name} \n"
                         f"uuid: {device_uuid}")
        if not device_name:
            device_name = device_uuid
        if device_name not in cls.connections.keys():
            conn = None
            if device_platform == 'Android':
                conn = AndroidDevice(device_uuid, device_platform, device_name)
            elif device_platform == 'iOS':
                conn = IOSDevice(device_uuid, device_platform, device_name)

            if conn:
                cls.connections[device_name] = conn
        else:
            conn = cls.connections[device_name]
            if conn.device_uuid != device_uuid:
                # 设备的 UUID 发生变化，需要重新连接
                conn.disconnect()
                if device_platform == 'Android':
                    conn = AndroidDevice(device_uuid, device_platform, device_name)
                elif device_platform == 'iOS':
                    conn = IOSDevice(device_uuid, device_platform, device_name)

                if conn:
                    cls.connections[device_name] = conn
        return conn


