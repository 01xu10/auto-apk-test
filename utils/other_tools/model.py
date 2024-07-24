# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/3/16 20:01
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : model.py
# ----------------------

from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel
from typing import Text, Dict, Union, Any


class NotificationType(Enum):
    """ 自动化通知方式 """
    DEFAULT = 0
    FEI_SHU = 1


@dataclass
class TestMetrics:
    """ 用例执行数据 """
    passed: int
    failed: int
    broken: int
    skipped: int
    total: int
    pass_rate: float
    time: Text


class ResponseData(BaseModel):
    url: Text
    response_data: Text
    request_body: Any
    method: Text
    headers: Dict
    res_time: Union[int, float]
    status_code: int


class PhoneInfo(BaseModel):
    platform: Text
    uuid: Text
    package: Text
    dev: Text


class Config(BaseModel):
    project_name: Text
    env: Text
    tester_name: Text
    notification_type: int = 0
    excel_report: bool
    mirror_source: Text
    email: "Email"
    lark: "Lark"
    allure_port: int


class Lark(BaseModel):
    webhook: Union[Text, None]
    secret: Union[Text, None]


class Email(BaseModel):
    send_user: Union[Text, None]
    email_host: Union[Text, None]
    stamp_key: Union[Text, None]
    # 收件人
    send_list: Union[Text, None]


class HttpFlow(BaseModel):
    flow_id: Text
    url: Text
    method: Text
    request_headers: Text
    request_content: Text
    status_code: int
    response_headers: Text
    response_content: Text

