# import cv2
#
# # 打开电脑摄像头
# cap = cv2.VideoCapture(0)
#
# while True:
#     # 获取摄像头画面
#     ret, frame = cap.read()
#
#     # 显示画面
#     cv2.rectangle(
#
#         frame,
#
#         (300, 200),
#
#         (600, 350),
#
#         (255, 0, 0),
#
#         2
#
#     )
#     cv2.imshow("Camera", frame)
#
#     # 按 q 键退出
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break
#
# # 关闭摄像头
# cap.release()
# cv2.destroyAllWindows()



import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # 获取画面的高度和宽度
    height, width = frame.shape[:2]

    # 设置识别框大小
    box_width = 300
    box_height = 150

    # 计算居中位置
    x1 = (width - box_width) // 2
    y1 = (height - box_height) // 2

    x2 = x1 + box_width
    y2 = y1 + box_height

    # 画框
    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        (255, 0, 0),
        2
    )
    #截取识别框里面的区域---ROI:Region of interest--感兴趣的区域
    roi = frame[y1:y2, x1:x2]
    #把彩色图像转换成灰度图
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    #二值化：
    _,binary = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    # 查找轮廓
    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    # 在 ROI 上画出轮廓
    contour_image = roi.copy()

    cv2.drawContours(
        contour_image,
        contours,
        -1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Contours", contour_image)

    #显示二值化结果：
    cv2.imshow('Binary', binary)
    #显示灰度图
    cv2.imshow("Gray", gray)
    #单独显示识别区域
    cv2.imshow('ROI', roi)

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()