# import cv2
#
# cap = cv2.VideoCapture(0)
#
# while True:
#     ret, frame = cap.read()
#
#     if not ret:
#         print("摄像头读取失败")
#         break
#
#     # 获取画面尺寸
#     height, width = frame.shape[:2]
#
#     # 设置框的大小
#     box_width = 300
#     box_height = 150
#
#     # 计算居中位置
#     x1 = (width - box_width) // 2
#     y1 = (height - box_height) // 2
#     x2 = x1 + box_width
#     y2 = y1 + box_height
#
#     # 画出 ROI 框
#     cv2.rectangle(
#         frame,
#         (x1, y1),
#         (x2, y2),
#         (255, 0, 0),
#         2
#     )
#
#     # 截取框里的区域
#     roi = frame[y1:y2, x1:x2]
#
#     # 显示
#     cv2.imshow("Camera", frame)
#     cv2.imshow("ROI", roi)
#
#     # 按 q 退出
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break
#
# cap.release()
# cv2.destroyAllWindows()

import cv2
import time
from paddleocr import PaddleOCR


# 创建 OCR
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    enable_mkldnn=False
)

# 打开摄像头
cap = cv2.VideoCapture(0)

last_ocr_time = 0

while True:
    ret, frame = cap.read()

    if not ret:
        print("摄像头读取失败")
        break

    # 获取画面尺寸
    height, width = frame.shape[:2]

    # 设置 ROI 大小
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

    # 截取 ROI
    roi = frame[y1:y2, x1:x2]

    # 每 2 秒识别一次
    current_time = time.time()

    if current_time - last_ocr_time >= 2:
        last_ocr_time = current_time

        result = ocr.predict(input=roi)

        for res in result:
            texts = res["rec_texts"]

            if texts:
                text = texts[0]
                print("识别到：", text)

    # 显示摄像头
    cv2.imshow("Camera", frame)

    # 显示 ROI
    cv2.imshow("ROI", roi)

    # 按 q 退出
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()