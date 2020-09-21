import cv2
import numpy as np
from matplotlib import pyplot as plt


# 原文：https://www.cnblogs.com/gezhuangzhuang/p/10724769.html
# 原文：https://blog.csdn.net/qq_21840201/article/details/85084621

# 1. 读入原图和模板
img_rgb = cv2.imread('bg.jpg')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('zan.jpg', 0)
h, w = template.shape[:2]

# 归一化平方差匹配
res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.8


# 返回res中值大于0.8的所有坐标
# 返回坐标格式(col,row) 注意：是先col后row 一般是(row,col)!!!
loc = np.where(res >= threshold)

# loc：标签/行号索引 常用作标签索引
# iloc：行号索引
# loc[::-1]：取从后向前（相反）的元素
# *号表示可选参数
for pt in zip(*loc[::-1]):
    right_bottom = (pt[0] + w, pt[1] + h)
    print(pt)
    cv2.rectangle(img_rgb, pt, right_bottom, (0, 0, 255), 2)

# 保存处理后的图片
cv2.imwrite('res.png', img_rgb)



# 显示图片 参数：（窗口标识字符串，imread读入的图像）
cv2.imshow("test_image", img_rgb)

# 窗口等待任意键盘按键输入 0为一直等待 其他数字为毫秒数
cv2.waitKey(0)

# 销毁窗口 退出程序
cv2.destroyAllWindows()