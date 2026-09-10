# import cv2
# import time
# from paddleocr import PaddleOCR
#
# # 创建 OCR
# ocr = PaddleOCR(
#     use_doc_orientation_classify=False,
#     use_doc_unwarping=False,
#     use_textline_orientation=False,
#     enable_mkldnn=False
# )
#
# # 打开摄像头
# cap = cv2.VideoCapture(0)
#
# # 上一次 OCR 的时间
# last_ocr_time = 0
#
# # 当前识别到的文字
# current_text = "等待识别..."
#
# while True:
#
#     ret, frame = cap.read()
#
#     if not ret:
#         print("摄像头读取失败")
#         break
#
#     # 获取画面尺寸
#     height, width = frame.shape[:2]
#
#     # ROI 大小
#     box_width = 300
#     box_height = 150
#
#     # 计算 ROI 位置
#     x1 = (width - box_width) // 2
#     y1 = (height - box_height) // 2
#     x2 = x1 + box_width
#     y2 = y1 + box_height
#
#     # 画出 ROI
#     cv2.rectangle(
#         frame,
#         (x1, y1),
#         (x2, y2),
#         (255, 0, 0),
#         2
#     )
#
#     # 截取 ROI
#     roi = frame[y1:y2, x1:x2]
#
#     # 每 2 秒 OCR 一次
#     current_time = time.time()
#
#     if current_time - last_ocr_time >= 2:
#
#         last_ocr_time = current_time
#
#         result = ocr.predict(input=roi)
#
#         for res in result:
#
#             texts = res["rec_texts"]
#
#             if texts:
#                 current_text = texts[0]
#
#                 print("识别到：", current_text)
#
#                 if ":" in current_text:
#
#                     minutes, seconds = current_text.split(":")
#
#                     total_seconds = int(minutes) * 60 + int(seconds)
#
#                     print("转换成秒：", total_seconds)
#
#                     # 开始倒计时
#                     while total_seconds >= 0:
#                         minutes = total_seconds // 60
#                         seconds = total_seconds % 60
#
#                         print(f"剩余时间：{minutes:02d}:{seconds:02d}")
#
#                         time.sleep(1)
#
#                         total_seconds -= 1
#
#     # 在画面上显示 OCR 结果
#     cv2.putText(
#         frame,
#         "OCR: " + current_text,
#         (50, 80),
#         cv2.FONT_HERSHEY_SIMPLEX,
#         1.2,
#         (0, 255, 0),
#         3
#     )
#
#     # 显示摄像头
#     cv2.imshow("Camera OCR", frame)
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

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    enable_mkldnn=False
)

cap = cv2.VideoCapture(0)

# OCR 上一次运行的时间
last_ocr_time = 0

# OCR 识别出的剩余时间
remaining_seconds = None

# Python 倒计时开始的时间
timer_start_time = None

while True:

    ret, frame = cap.read()

    if not ret:
        print("摄像头读取失败")
        break

    # =========================
    # 1. ROI
    # =========================

    height, width = frame.shape[:2]

    box_width = 300
    box_height = 150

    x1 = (width - box_width) // 2
    y1 = (height - box_height) // 2
    x2 = x1 + box_width
    y2 = y1 + box_height

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        (255, 0, 0),
        2
    )

    roi = frame[y1:y2, x1:x2]

    # =========================
    # 2. OCR 每 2 秒校准
    # =========================

    now = time.time()

    if now - last_ocr_time >= 2:

        last_ocr_time = now

        result = ocr.predict(input=roi)

        for res in result:

            texts = res["rec_texts"]

            if texts:

                text = texts[0]

                print("OCR识别：", text)

                if ":" in text:

                    try:

                        minutes, seconds = text.split(":")

                        new_time = (
                            int(minutes) * 60
                            + int(seconds)
                        )

                        remaining_seconds = new_time

                        timer_start_time = time.time()

                        print(
                            "时间校准：",
                            f"{minutes}:{seconds}"
                        )

                    except ValueError:

                        print("时间格式错误")

    # =========================
    # 3. 实时计算剩余时间
    # =========================

    if remaining_seconds is not None:

        elapsed = time.time() - timer_start_time

        display_seconds = max(
            0,
            int(remaining_seconds - elapsed)
        )

        minutes = display_seconds // 60
        seconds = display_seconds % 60

        timer_text = (
            f"Remaining: "
            f"{minutes:02d}:{seconds:02d}"
        )

    else:

        timer_text = "Waiting for OCR..."

    # =========================
    # 4. 显示时间
    # =========================

    cv2.putText(
        frame,
        timer_text,
        (50, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 255, 0),
        3
    )

    # 显示摄像头
    cv2.imshow(
        "Camera OCR Timer",
        frame
    )

    # q 退出
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()