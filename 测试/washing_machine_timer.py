import cv2
import time
import re
from paddleocr impofrt PaddleOCR


# ============================================================
# 1. 初始化 OCR
# ============================================================

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    enable_mkldnn=False
)


# ============================================================
# 2. 打开摄像头
# ============================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("无法打开摄像头")
    exit()


# ============================================================
# 3. 程序变量
# ============================================================

# 上一次 OCR 的时间
last_ocr_time = 0

# OCR 间隔
OCR_INTERVAL = 2

# 当前剩余时间
remaining_seconds = None

# 上一次成功 OCR 的时间
timer_start_time = None

# 当前 OCR 识别结果
ocr_text = "等待识别..."

# 程序运行状态
status_text = "正在等待洗衣机时间..."


# ============================================================
# 4. 时间文字转换函数
# ============================================================

def parse_time(text):

    """
    将 OCR 识别出的文字转换成秒。

    例如：
    21:01 → 1261
    09:30 → 570
    """

    # 去掉空格
    text = text.strip()#strip的作用：去掉字符串两边多余的空格

    # OCR 有时候会识别成 21.01
    text = text.replace(".", ":")#帮它纠正

    # OCR 有时候会识别成中文冒号
    text = text.replace("：", ":")

    # 查找类似 21:01 的格式
    match = re.search(r"(\d{1,2}):(\d{1,2})", text)

    if not match:
        return None

    minutes = int(match.group(1))
    seconds = int(match.group(2))

    # 秒数不应该超过 59
    if seconds >= 60:
        return None

    # 防止出现非常离谱的分钟数
    if minutes > 99:
        return None

    total_seconds = minutes * 60 + seconds

    return total_seconds


# ============================================================
# 5. 主循环
# ============================================================

while True:

    # --------------------------------------------------------
    # 读取摄像头
    # --------------------------------------------------------

    ret, frame = cap.read()

    if not ret:
        print("摄像头读取失败")
        break


    # ========================================================
    # 6. 获取画面尺寸
    # ========================================================

    height, width = frame.shape[:2]


    # ========================================================
    # 7. 设置 ROI
    # ========================================================

    box_width = 300
    box_height = 150

    x1 = (width - box_width) // 2
    y1 = (height - box_height) // 2

    x2 = x1 + box_width
    y2 = y1 + box_height


    # ========================================================
    # 8. 绘制 ROI 框
    # ========================================================

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        (255, 0, 0),
        2
    )


    # ========================================================
    # 9. 截取 ROI
    # ========================================================

    roi = frame[y1:y2, x1:x2]


    # ========================================================
    # 10. OCR
    # ========================================================

    now = time.time()

    if now - last_ocr_time >= OCR_INTERVAL:

        last_ocr_time = now

        try:

            result = ocr.predict(input=roi)#OCP，帮我看看这张图片里写了什么

            found_time = False

            for res in result:

                texts = res["rec_texts"]

                if not texts:
                    continue

                # OCR 可能返回多个文字
                for text in texts:

                    print("OCR识别：", text)

                    parsed_time = parse_time(text)

                    if parsed_time is not None:

                        # 成功识别
                        remaining_seconds = parsed_time

                        timer_start_time = time.time()

                        ocr_text = text

                        status_text = "OCR 已成功识别"

                        found_time = True

                        print(
                            "识别成功：",
                            text,
                            "→",
                            parsed_time,
                            "秒"
                        )

                        break

                if found_time:
                    break

            if not found_time:

                status_text = "OCR 未识别到有效时间"

                print("本次 OCR 没有识别到有效时间")

        except Exception as e:

            print("OCR 出现错误：", e)

            status_text = "OCR 暂时失败"


    # ========================================================
    # 11. 计算实时剩余时间
    # ========================================================

    if remaining_seconds is not None and timer_start_time is not None:

        elapsed = time.time() - timer_start_time

        display_seconds = max(
            0,
            int(remaining_seconds - elapsed)
        )

        minutes = display_seconds // 60
        seconds = display_seconds % 60

        timer_text = f"{minutes:02d}:{seconds:02d}"

    else:

        timer_text = "--:--"


    # ========================================================
    # 12. 显示「剩余时间」
    # ========================================================

    cv2.putText(
        frame,
        "Remaining Time",
        (30, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        timer_text,
        (30, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.8,
        (0, 255, 0),
        4
    )


    # ========================================================
    # 13. 显示 OCR 状态
    # ========================================================

    cv2.putText(
        frame,
        status_text,
        (30, height - 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 255),
        2
    )


    # ========================================================
    # 14. 显示摄像头画面
    # ========================================================

    cv2.imshow(
        "Washing Machine Timer",
        frame
    )


    # ========================================================
    # 15. 按 Q 退出
    # ========================================================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ============================================================
# 16. 释放资源
# ============================================================

cap.release()

cv2.destroyAllWindows()

print("程序已退出")