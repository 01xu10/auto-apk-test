# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/7/13 10:47
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : apk_control.py
# ----------------------
from pprint import pprint

import xmltodict
from apkutils import APK


class ApkUtils:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_package_name(self):
        with APK.from_file(self.file_path) as apk:
            apk.parse_resouce()
            package_name = apk.get_package_name()
        return package_name

    def get_manifest(self):
        """
        获取 AndroidManifest.xml 信息
        :return: manifest
        """
        with APK.from_file(self.file_path) as apk:
            apk._init_manifest()
            manifest = apk.get_manifest()
        return manifest

    def get_manual_high_permissions(self):
        """
        获取apk运行时所需的设备权限
        :return: manual_high_permissions
        """
        manifest_xml = self.get_manifest()
        manifest_dict = xmltodict.parse(manifest_xml)
        permissions = manifest_dict.get('manifest', {}).get('uses-permission', [])

        manual_high_permissions = []

        for permission in permissions:
            permission_name = permission.get('@android:name', '')
            if self.is_manual_high_permission(permission_name):
                manual_high_permissions.append(permission_name)

        return manual_high_permissions

    def get_meta_data(self, name):
        """
        获取 AndroidManifest.xml meta-data
        :return: value
        """
        manifest_xml = self.get_manifest()
        manifest_dict = xmltodict.parse(manifest_xml)
        meta_datas = manifest_dict.get('manifest', {}).get('application', {}).get('meta-data')
        for meta_data in meta_datas:
            if name == meta_data.get('@android:name'):
                value = meta_data.get('@android:value')
                return value

    def is_manual_high_permission(self, permission_name):
        if self.is_runtime_permission(permission_name):
            return True
        return False

    @staticmethod
    def is_runtime_permission(permission_name):
        runtime_permissions = [
            "android.permission.READ_CALENDAR",
            "android.permission.WRITE_CALENDAR",
            "android.permission.CAMERA",
            "android.permission.READ_CONTACTS",
            "android.permission.WRITE_CONTACTS",
            "android.permission.GET_ACCOUNTS",
            "android.permission.ACCESS_FINE_LOCATION",
            "android.permission.ACCESS_COARSE_LOCATION",
            "android.permission.RECORD_AUDIO",
            "android.permission.READ_PHONE_STATE",
            "android.permission.CALL_PHONE",
            "android.permission.READ_CALL_LOG",
            "android.permission.WRITE_CALL_LOG",
            "android.permission.ADD_VOICEMAIL",
            "android.permission.USE_SIP",
            "android.permission.PROCESS_OUTGOING_CALLS",
            "android.permission.BODY_SENSORS",
            "android.permission.SEND_SMS",
            "android.permission.RECEIVE_SMS",
            "android.permission.READ_SMS",
            "android.permission.RECEIVE_WAP_PUSH",
            "android.permission.RECEIVE_MMS",
            "android.permission.READ_EXTERNAL_STORAGE",
            "android.permission.MEDIA_CONTENT_CONTROL",
            "android.permission.WRITE_EXTERNAL_STORAGE"
        ]

        return permission_name in runtime_permissions
