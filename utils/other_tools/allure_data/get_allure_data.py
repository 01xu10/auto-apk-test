# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/4/10 19:13
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : get_allure_data.py
# ----------------------
import json

from common import ensure_path_sep
from utils.other_tools.model import TestMetrics


class AllureFileClean:
    """allure 报告数据清洗，提取业务需要得数据"""

    @classmethod
    def get_case_count(cls) -> "TestMetrics":
        """ 统计用例数量 """
        try:
            file_name = ensure_path_sep("\\reports\\allure_reports\\html\\widgets\\summary.json")
            with open(file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
            _case_count = data['statistic']
            _time = data['time']
            keep_keys = {"passed", "failed", "broken", "skipped", "total"}
            run_case_data = {k: v for k, v in data['statistic'].items() if k in keep_keys}
            # 判断运行用例总数大于0
            if _case_count["total"] > 0:
                # 计算用例成功率
                run_case_data["pass_rate"] = round(
                    (_case_count["passed"] + _case_count["skipped"]) / _case_count["total"] * 100, 2
                )
            else:
                # 如果未运行用例，则成功率为 0.0
                run_case_data["pass_rate"] = 0.0
            # 收集用例运行时长
            run_case_data['time'] = _time if run_case_data['total'] == 0 else round(_time['duration'] / 1000, 2)
            return TestMetrics(**run_case_data)
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                "程序中检查到您未生成allure报告，"
                "通常可能导致的原因是allure环境未配置正确，"
                "详情可查看如下博客内容："
                "https://blog.csdn.net/weixin_43865008/article/details/124332793"
            ) from exc
