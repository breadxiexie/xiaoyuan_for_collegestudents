import re
import time
from paddleocr import PaddleOCR
import pyautogui
import numpy as np

# 初始化 OCR 模型
ocr = PaddleOCR(use_angle_cls=True, lang="en")  # 如果识别英文

#  使用screen_location程序获得OCR识别区坐标（注意！！！区域坐标需要根据实际情况调整）
ocr_top_left = (ocr_x1, ocr_y1) =(273, 320) # OCR区左上角坐标
ocr_top_right = (ocr_x2, ocr_y2) =(545, 333)  # OCR区右上角坐标
ocr_bottom_left = (ocr_x3, ocr_y3) =(290, 390)  # OCR区左下角坐标
ocr_bottom_right = (ocr_x4, ocr_y4)=(526, 398)   # OCR区右下角坐标

# 计算OCR区域的左上角和右下角坐标
ocr_left_top = (min(ocr_top_left[0], ocr_top_right[0], ocr_bottom_left[0], ocr_bottom_right[0]),
                min(ocr_top_left[1], ocr_top_right[1], ocr_bottom_left[1], ocr_bottom_right[1]))
ocr_right_bottom = (max(ocr_top_left[0], ocr_top_right[0], ocr_bottom_left[0], ocr_bottom_right[0]),
                    max(ocr_top_left[1], ocr_top_right[1], ocr_bottom_left[1], ocr_bottom_right[1]))

# 设置需要捕获的屏幕区域坐标 (左, 上, 宽, 高)
ocr_screen_bbox = (ocr_left_top[0], ocr_left_top[1],
                   ocr_right_bottom[0] - ocr_left_top[0], ocr_right_bottom[1] - ocr_left_top[1])

#  使用screen_location程序获得绘制区坐标（注意！！！区域坐标需要根据实际情况调整）
draw_top_left = (draw_x1, draw_y1)  =(241,546)# 绘制区左上角坐标
draw_top_right = (draw_x2, draw_y2)  =(574,554)# 绘制区右上角坐标
draw_bottom_left = (draw_x3, draw_y3)  =(244,713)# 绘制区左下角坐标
draw_bottom_right = (draw_x4, draw_y4)  =(544,733)# 绘制区右下角坐标

# 设置识别间隔时间（秒）
interval_seconds = 0.3


def extract_digits(text):
    # 使用正则表达式匹配数字
    digits = re.findall(r'\d+', text)
    # 将匹配到的数字转换为整数
    numbers = [int(digit) for digit in digits]
    return numbers


def draw_greater_than(top_left, top_right, bottom_left, bottom_right):
    """
    绘制大于号 (>).
    从左上角移动到右上角和右下角连线的中点，
    再移动到左下角。
    """
    mid_point = ((top_right[0] + bottom_right[0]) / 2, top_right[1])

    # 按住鼠标左键开始绘制
    pyautogui.mouseDown(x=top_left[0], y=top_left[1])
    pyautogui.moveTo(mid_point[0], mid_point[1])
    pyautogui.moveTo(bottom_left[0], bottom_left[1])
    pyautogui.mouseUp()


def draw_less_than(top_right, top_left, bottom_left, bottom_right):
    """
    绘制小于号 (<).
    从右上角移动到左上角和左下角连线的中点，
    再移动到右下角。
    """
    mid_point = ((top_left[0] + bottom_left[0]) / 2, top_left[1])

    # 按住鼠标左键开始绘制
    pyautogui.mouseDown(x=top_right[0], y=top_right[1])
    pyautogui.moveTo(mid_point[0], mid_point[1])
    pyautogui.moveTo(bottom_right[0], bottom_right[1])
    pyautogui.mouseUp()


def capture_and_ocr(bbox):
    # 捕获屏幕上的指定区域
    screenshot = pyautogui.screenshot(region=bbox)
    # 转换为 numpy 数组
    img = np.array(screenshot)
    # 使用 PaddleOCR 进行 OCR 识别
    result = ocr.ocr(img, cls=True)

    # 输出识别结果
    if result and len(result) > 0:
        all_texts = []
        # 假设结果的第一个列表包含所有的检测框信息
        for detection in result[0]:
            if isinstance(detection, list) and len(detection) == 2:
                _, (text, _) = detection
                all_texts.append(text)
                print(f'Text: {text}')

        # 合并所有文本
        combined_text = ' '.join(all_texts)

        # 提取数字
        numbers = extract_digits(combined_text)

        # 分别存储到 a 和 b 变量中
        if len(numbers) >= 2:
            a, b = numbers[:2]
            print(f'a = {a}, b = {b}')

            # 比较 a 和 b 的大小，并绘制相应的符号
            if a > b:
                print('绘制大于号')
                draw_greater_than(draw_top_left, draw_top_right, draw_bottom_left, draw_bottom_right)
            elif a < b:
                print('绘制小于号')
                draw_less_than(draw_top_right, draw_top_left, draw_bottom_left, draw_bottom_right)
            else:
                print('a 和 b 相等')
        elif len(numbers) == 1:
            a = numbers[0]
            b = None
            print(f'a = {a}, b = None')
        else:
            a = None
            b = None
            print('未找到数字')
    else:
        print('未检测到任何文本')


# 主循环
if __name__ == "__main__":
    while True:
        try:
            capture_and_ocr(ocr_screen_bbox)
        except Exception as e:
            print(f'发生错误：{e}')
        time.sleep(interval_seconds)