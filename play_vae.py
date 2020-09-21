import os
import cv2
import numpy as np
import time
import random


# 使用的Python库及对应版本：
# python 3.6
# opencv-python 3.3.0
# numpy 1.13.3
# 用到了opencv库中的模板匹配和边缘检测功能
#Author:火流星

def get_screenshot(id):
    os.system('adb shell screencap -p /sdcard/%s.png' % str(id))
    os.system('adb pull /sdcard/%s.png .' % str(id))


def tap(x,y):
    # 这个参数还需要针对屏幕分辨率进行优化
    #press_time = int(distance * 1.35)

    # 生成随机手机屏幕模拟触摸点
    # 模拟触摸点如果每次都是同一位置，可能无法通过验证
    rand = random.randint(0, 9) * 10
    cmd = ('adb shell input tap %i %i ') \
          % (x+100, y)
    os.system(cmd)
    print(cmd)

def swap():
    #滑动屏幕
    cmd = ('adb shell input swipe %i %i %i %i ' ) \
          % (500, 1000, 500, 300)
    os.system(cmd)

def get_center(img_canny, ):
    # 利用边缘检测的结果寻找物块的上沿和下沿
    # 进而计算物块的中心点
    y_top = np.nonzero([max(row) for row in img_canny[400:]])[0][0] + 400
    x_top = int(np.mean(np.nonzero(canny_img[y_top])))

    y_bottom = y_top + 50
    for row in range(y_bottom, H):
        if canny_img[row, x_top] != 0:
            y_bottom = row
            break

    x_center, y_center = x_top, (y_top + y_bottom) // 2
    return img_canny, x_center, y_center


def matchImg(img_rgb,tmp):
    res1 = cv2.matchTemplate(img_rgb, tmp, cv2.TM_CCOEFF_NORMED)
    min_val1, max_val, min_loc1, max_loc1 = cv2.minMaxLoc(res1)
    center1_loc = (max_loc1[0], max_loc1[1])
    print("匹配结果：",center1_loc)
    return max_val,max_loc1[0],max_loc1[1]

print("火流星")
time.sleep(1)
# 匹配的模板
temp1 = cv2.imread('vae/zan.jpg', 0)
w1, h1 = temp1.shape[::-1]


# 循环10000次
for i in range(10000):
    get_screenshot(0)
    img_rgb = cv2.imread('%s.png' % 0, 0)


    # res_end = cv2.matchTemplate(img_rgb, temp_end, cv2.TM_CCOEFF_NORMED)
    # if cv2.minMaxLoc(res_end)[1] > 0.95:
    #     print('Game over!')
    #     break

    # 模板匹配截图中的位置
    max_val1,max_x,max_y=matchImg(img_rgb,temp1)

    if max_val1 > 0.95:
        print('found white circle!')
        x_center, y_center = max_x, max_y
        tap(x_center, y_center)
        max_val1, max_x, max_y = matchImg(img_rgb, temp1)
    else:
        swap()
    # 将图片输出以供调试
    # img_rgb = cv2.circle(img_rgb, (x_center, y_center), 10, 255, -1)
    # # cv2.rectangle(canny_img, max_loc1, center1_loc, 255, 2)
    # cv2.imwrite('last.png', img_rgb)


    time.sleep(0.2)
