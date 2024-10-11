import pyautogui
import time

try:
    # 设置一个暂停时间，以便让程序有时间显示输出
    time.sleep(2)

    print("按Ctrl+C停止")

    while True:
        # 获取鼠标当前位置
        x, y = pyautogui.position()

        # 直接打印出来，不使用'\r'
        print(f"鼠标位置: X={x}, Y={y}")
        time.sleep(0.1)  # 等待0.1秒后再次检查鼠标位置
except KeyboardInterrupt:
    print("\n停止了程序。")