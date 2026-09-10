import time
from paddleocr import PaddleOCR


# 创建 OCR
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    enable_mkldnn=False
)


# 识别图片
result = ocr.predict(input="IMG_1938.jpeg")


# 获取识别结果
for res in result:

    texts = res["rec_texts"]

    if texts:

        text = texts[0]

        print("OCR识别：", text)

        # 判断是不是类似 21:01 的格式
        if ":" in text:

            minutes, seconds = text.split(":")

            total_seconds = int(minutes) * 60 + int(seconds)

            print("转换成秒：", total_seconds)

            # 开始倒计时
            while total_seconds >= 0:

                minutes = total_seconds // 60
                seconds = total_seconds % 60

                print(f"剩余时间：{minutes:02d}:{seconds:02d}")

                time.sleep(1)

                total_seconds -= 1