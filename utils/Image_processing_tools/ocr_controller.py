# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/4/19 10:22
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : ocr_controller.py
# ----------------------
import io
import math
from PIL import Image
import allure
import cv2
import ddddocr
from common.setting import ensure_path_sep
from airtest.aircv import aircv
from utils.logging_tools.log_controller import ERROR, INFO
from common.action import snapshot


@allure.step("检测文本->缩放图片")
def cut_text_region(image_path, padding=1):
    """
    对指定图片进行文字区域裁剪

    Args:
        image_path (str): 待处理图片路径
        padding (int): 文本框上下留白像素数

    """
    try:
        # 加载 ddddocr 模型
        ocr = ddddocr.DdddOcr(det=True)
        with open(image_path, 'rb') as f:
            image = f.read()
        # 使用 ddddocr 进行文本检测，获取文本框的位置信息
        INFO.logger.info("正在进行文本检测...")
        result = ocr.detection(image)
        # rectangle_p(image_path, result)
        cut_p(image_path, padding, result)

    except Exception as e:
        snapshot(is_error=True)
        ERROR.logger.info("无法对空图像进行缩放！")
        raise RuntimeError("文本检测失败，没有检测出文本信息 error log: {}".format(e))


def rectangle_p(image_path, result):
    im = cv2.imread(image_path)
    # 圈出文字
    for box in result:
        x1, y1, x2, y2 = box
        im = cv2.rectangle(im, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)
    import datetime
    now_time = datetime.datetime.now().strftime(r'%Y-%m-%d_%H-%M-%S')
    save_path = ensure_path_sep("\\out_files\\snapshot\\check\\{}.png".format(now_time))
    # cv2.imwrite(save_path, im)
    cv2.imwrite(save_path, im, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
    with open(save_path, "rb") as f:
        file_content = f.read()
    allure.attach(file_content, name="rectangleText", attachment_type=allure.attachment_type.PNG)


def cut_p(image_path, padding, result):
    im2 = cv2.imread(image_path)
    # im2 = aircv.imread(image_path)
    min_y, max_y = float("inf"), float("-inf")
    # 遍历获取到的文本框，取出其纵向位置范围
    for box in result:
        _, y1, _, y2 = box
        if not math.isinf(y1):
            min_y = min(min_y, y1)
        if not math.isinf(y2):
            max_y = max(max_y, y2)
    # 根据纵向位置范围对图像进行裁剪
    text_region = im2[int(min_y - padding): int(max_y + padding)]
    if text_region.any():
        aircv.imwrite(image_path, text_region, 99)
        # text_region = cv2.resize(text_region, (text_region.shape[1] // 2, text_region.shape[0] // 2))
        # cv2.imwrite(image_path, text_region)
        # cv2.imwrite(image_path, text_region, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
        with open(image_path, "rb") as f:
            file_content = f.read()
        allure.attach(file_content, name="final screenshot", attachment_type=allure.attachment_type.PNG)

    else:
        raise ValueError("无法对空图像进行缩放")


@allure.step("识别文本")
def recognize_text(image_path):
    """
    识别图片中的文本

    Args:
        image_path (str): 待处理图片路径

    Returns:
        res (str): 识别出的文本信息，若识别失败则返回空字符串
    """
    try:
        ocr = ddddocr.DdddOcr(old=True)
        img = Image.open(image_path)
        imgByteArr = io.BytesIO()
        img.save(imgByteArr, format='JPEG')
        imgByteArr = imgByteArr.getvalue()
        res = ocr.classification(imgByteArr)
        allure.attach("识别信息", res)
    except Exception as e:
        snapshot(is_error=True)
        ERROR.logger.error("文本识别失败，没有识别出文本信息 error log: {}".format(e))
        raise ValueError('文本识别失败，没有识别出文本信息')
    return res


# if __name__ == '__main__':
#     from common.setting import ensure_path_sep
#     path = ensure_path_sep("\\out_files\\snapshot\\normal\\2023-07-13_14-01-08.png")
#     path2 = ensure_path_sep("\\out_files\\snapshot\\normal\\2023-07-13_14-04-54.png")
#     # cut_text_region(path)
#     print(recognize_text(path))
#     print(recognize_text(path2))
