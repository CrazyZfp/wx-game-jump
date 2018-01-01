from subprocess import check_output
import io
import time
from math import floor

MS_PER_PIX = 1.4


# 先保存图片
def get_cap_path():
    pname = floor(time.time())
    ppath = "/home/zfp/Coding/Projects/wx-game-controller/pic/{}.png".format(pname)
    check_output(r"/home/zfp/Apps/adb/platform-tools/adb shell screencap -p | sed 's/\r\n/\n/g' >> {}".format(ppath),
                 shell=True)
    return ppath


# 获取截屏图片数据流
def get_cap_bytes():
    pname = floor(time.time())
    # ppath = "/home/zfp/Coding/Projects/wx-game-controller/pic/{}.png".format(pname)
    raw = check_output(r"/home/zfp/Apps/adb/platform-tools/adb shell screencap -p | sed 's/\r\n/\n/g'", shell=True)
    return io.BytesIO(raw)
    # check_output(r"/home/zfp/Apps/adb/platform-tools/adb shell screencap -p | sed 's/\r\n/\n/g' >> {}".format(ppath),
    #              shell=True)
    # return ppath


def press_screen(milliseconds):
    print(milliseconds)
    check_output("adb shell input swipe 500 500 500 500 {}".format(milliseconds), shell=True)


def jump_pixel(pixels):
    print(pixels)
    milliseconds = pixels * MS_PER_PIX
    press_screen(round(milliseconds))
