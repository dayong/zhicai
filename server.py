from flask import Flask, request
from flask_cors import CORS
import pyautogui
import random
import time
import math

app = Flask(__name__)
CORS(app)  # 允许跨域



def bezier_curve(p0, p1, p2, p3, steps=100):
    """生成三次贝塞尔曲线轨迹"""
    points = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
        y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
        points.append((x, y))
    return points


def ease_in_out_quad(t):
    """缓动函数：加速-减速"""
    return 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t


# 从一个点到另一个点

def human_like_move_from_to(target_x, target_y, duration=1.0):
    """模拟人类鼠标移动"""
    # 随机控制点，保证曲线不是直线
    start_x, start_y = pyautogui.position()

    print('target_x, target_y', target_x, target_y)

    print('start_x, start_y',start_x, start_y)


    cp1 = (start_x + (target_x - start_x) * random.uniform(0.3, 0.5) + random.randint(-100, 100),
           start_y + (target_y - start_y) * random.uniform(0.3, 0.5) + random.randint(-100, 100))
    cp2 = (start_x + (target_x - start_x) * random.uniform(0.5, 0.8) + random.randint(-100, 100),
           start_y + (target_y - start_y) * random.uniform(0.5, 0.8) + random.randint(-100, 100))

    steps = random.randint(50, 60)
    path = bezier_curve((start_x, start_y), cp1, cp2, (target_x, target_y), steps)

    start_time = time.time()
    for i in range(steps + 1):
        t = i / steps
        eased_t = ease_in_out_quad(t)  # 应用加速减速
        index = int(eased_t * steps)
        x, y = path[index]

        try:
            pyautogui.moveTo(x, y)
        except pyautogui.FailSafeException:
            print('出界')
        

        # 保持总时长接近 duration
        elapsed = time.time() - start_time
        expected = eased_t * duration
        sleep_time = expected - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)


# 模拟点击
def human_click(x, y, move_duration=(0.1, 0.2), press_duration=(0.07, 0.35), offset=2):
    """
    模拟人类点击动作，保证触发浏览器 click
    x, y : 目标坐标
    move_duration : 鼠标移动耗时范围 (秒)
    press_duration : mousedown -> mouseup 停留时间范围 (秒)
    offset : 坐标随机偏移，模拟手抖 (像素)
    """

    # 随机偏移坐标
    target_x = x + random.randint(-offset, offset)
    target_y = y + random.randint(-offset, offset)

    # 平滑移动到目标位置
    duration = random.uniform(*move_duration)
    pyautogui.moveTo(x, y, duration=duration)

    # 按下鼠标
    pyautogui.mouseDown()

    # 按下保持随机时间
    press_time = random.uniform(*press_duration)
    time.sleep(press_time)

    # 抬起鼠标，触发 click
    pyautogui.mouseUp()

    print(f"Clicked at ({target_x}, {target_y}) | move_duration={duration:.2f}s | press_duration={press_time:.2f}s")




# 模拟人类打字
def human_typing(text):
    for char in text:
        pyautogui.write(char)
        time.sleep(random.uniform(0.05, 0.2))  # 随机延迟模拟自然输入


# 模拟随机滑动几次鼠标
def random_scroll_cursor():
    count = random.randint(0, 2)
    screenWidth, screenHeight = pyautogui.size()

    if count > 0:
        for num in range(0, count):
            to_x = random.randint(300, screenWidth - 300)
            to_y = random.randint(200, screenHeight - 200)
            human_like_move_from_to(to_x, to_y, duration=random.uniform(0.1, 0.5))

            press_time = random.uniform(0.2, 0.8)
            time.sleep(press_time)
    




        



@app.route("/click", methods=["POST"])
def click():
    data = request.json
    x, y = data.get("x"), data.get("y")
    print(f'{x}|{y}')
    if x is None or y is None:
        return {"status": "error", "message": "缺少坐标"}, 400

    # 移动鼠标并点击
    print(f'移动鼠标并点击{x}|{y}')

    # 随机移动几次鼠标
    # random_scroll_cursor()

    # 1. 随机移动鼠标到

    human_like_move_from_to(x, y, duration=0.1)


    # 2. 模拟点击
    human_click(x, y)

    press_time = random.uniform(0.3, 1)
    time.sleep(press_time)


    screenWidth, screenHeight = pyautogui.size()

    print(screenWidth, screenHeight)

    to_x = random.randint(int(screenWidth/2), screenWidth - 1)
    to_y = random.randint(100, screenHeight - 100)

    # 点击后 移走
    # random_move_to(to_x, to_y, 0.2)
    # pyautogui.moveTo(screenWidth/2, screenHeight/2, duration=0.5)


    human_like_move_from_to(to_x, to_y, duration=random.uniform(0.1, 0.6))
    
   
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(port=5000)