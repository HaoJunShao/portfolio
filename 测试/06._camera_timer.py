import cv2
import time

# 假设洗衣机剩余 21 分 01 秒
total_seconds = 21 * 60 + 1

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        print("摄像头读取失败")
        break

    # 计算分钟和秒
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    # 在画面上显示剩余时间
    text = f"Remaining: {minutes:02d}:{seconds:02d}"

    cv2.putText(
        frame,
        text,
        (50, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.5,
        (0, 255, 0),
        3
    )

    # 显示摄像头
    cv2.imshow("Camera Timer", frame)

    # 每秒倒计时一次
    time.sleep(1)
    total_seconds -= 1

    # 按 q 退出
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()