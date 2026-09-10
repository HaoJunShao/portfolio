# text = "21:01"
#
# minutes, seconds = text.split(":")#把分钟和秒钟拆开，并进行分别赋值
#
# total_seconds = int(minutes) * 60 + int(seconds)
#
# print("分钟：", minutes)
# print("秒：", seconds)
# print("总秒数：", total_seconds)
import time

total_seconds = 10

while total_seconds >= 0:

    minutes = total_seconds // 60
    seconds = total_seconds % 60

    print(f"{minutes:02d}:{seconds:02d}")

    time.sleep(1)#让程序暂停1秒

    total_seconds -= 1