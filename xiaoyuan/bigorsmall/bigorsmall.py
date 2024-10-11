import ocr
import time
import re
from paddleocr import PaddleOCR
import pyautogui
import numpy as np
# 使用screen_location程序获得四个顶点坐标
top_left = (x1,y1)=(288, 330)  # 左上角坐标
top_right = (x2,y2)=(525, 332)  # 右上角坐标
bottom_left =(x3,y3)= (295, 394)  # 左下角坐标
bottom_right = (x4,y4)=(521, 400)  # 右下角坐标

# 计算左上角和右下角坐标
left_top = (min(x1, x2, x3, x4), min(y1, y2, y3, y4))
right_bottom = (max(x1, x2, x3, x4), max(y1, y2, y3, y4))

# 设置需要捕获的屏幕区域坐标 (左, 上, 宽, 高)
screen_bbox = (left_top[0], left_top[1], right_bottom[0] - left_top[0], right_bottom[1] - left_top[1])

a,b=ocr.capture_and_ocr(screen_bbox)