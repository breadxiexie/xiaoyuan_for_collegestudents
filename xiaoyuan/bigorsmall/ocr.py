import time
import re
from paddleocr import PaddleOCR
import pyautogui
import numpy as np
# 初始化 OCR 模型
ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # 如果识别中文
# ocr = PaddleOCR(use_angle_cls=True, lang="en")  # 如果识别英文

#  使用screen_location程序获得四个顶点坐标
top_left = (x1,y1)=(288, 330)  # 左上角坐标
top_right = (x2,y2)=(525, 332)  # 右上角坐标
bottom_left =(x3,y3)= (295, 394)  # 左下角坐标
bottom_right = (x4,y4)=(521, 400)  # 右下角坐标

# 计算左上角和右下角坐标
left_top = (min(x1, x2, x3, x4), min(y1, y2, y3, y4))
right_bottom = (max(x1, x2, x3, x4), max(y1, y2, y3, y4))

# 设置需要捕获的屏幕区域坐标 (左, 上, 宽, 高)
screen_bbox = (left_top[0], left_top[1], right_bottom[0] - left_top[0], right_bottom[1] - left_top[1])

# 设置识别间隔时间（秒）
interval_seconds = 2


def extract_digits(text):
    # 使用正则表达式匹配数字
    digits = re.findall(r'\d+', text)
    # 将匹配到的数字转换为整数
    numbers = [int(digit) for digit in digits]
    return numbers


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

        for detection in result[0]:
            if isinstance(detection, list) and len(detection) == 2:
                _, (text, _) = detection
                all_texts.append(text)
                print(f'Text: {text}')


        combined_text = ' '.join(all_texts)

        # 提取数字
        numbers = extract_digits(combined_text)

        # 分别存储到 a 和 b 变量中
        if len(numbers) >= 2:
            a, b = numbers[:2]
            print(f'a = {a}, b = {b}')
            return a, b
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
            capture_and_ocr(screen_bbox)
        except Exception as e:
            print(f'发生错误：{e}')
        time.sleep(interval_seconds)