# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/7/13 9:41
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : test.py
# ----------------------
import io
from common.setting import ensure_path_sep
import ddddocr
from PIL import Image


class getVerifyCode:
    ocr = ddddocr.DdddOcr(old=True)

    def getCodeByReqImage(self,path):
        img = Image.open(path)
        imgByteArr = io.BytesIO()
        img.save(imgByteArr, format='JPEG')
        imgByteArr = imgByteArr.getvalue()
        code = self.ocr.classification(imgByteArr)
        return code


if __name__ == '__main__':
    getcode = getVerifyCode()
    code = getcode.getCodeByReqImage(ensure_path_sep("\\out_files\\snapshot\\cut\\2023-07-12_18-18-46.png"))
    print(code)
    # print(None)