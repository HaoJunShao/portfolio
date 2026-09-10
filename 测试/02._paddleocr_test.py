from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    enable_mkldnn=False,
)

result = ocr.predict(input="IMG_1938.jpeg")

for res in result:
    print(res["rec_texts"])