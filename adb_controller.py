from subprocess import check_output
import io
import time
from math import floor

MS_PER_PIX = 1.4    # 1px距离需要长按约1.4ms

ADB_PATH = "/home/zfp/Apps/adb/platform-tools/adb"
PIC_DIR = "/home/zfp/Coding/Projects/wx-game-controller/pic"


def get_cap_path():
    """
    先保存图片，再进行操作。用于DEBUG。
    :return: 本次截屏图片的保存地址
    """
    pname = floor(time.time())
    ppath = "{pic_dir}/{pic_name}.png".format(pic_dir=PIC_DIR, pic_name=pname)
    check_output(
        r"{adb_path} shell screencap -p | sed 's/\r\n/\n/g' >> {pic_path}".format(adb_path=ADB_PATH, pic_path=ppath),
        shell=True)
    return ppath


def get_cap_bytes():
    """
    获取截屏图片数据流，直接操作不保存。
    """
    raw = check_output(r"{adb_path} shell screencap -p | sed 's/\r\n/\n/g'".format(adb_path=ADB_PATH), shell=True)
    return io.BytesIO(raw)


def press_screen(milliseconds):
    print(milliseconds)
    check_output("adb shell input swipe 500 500 500 500 {}".format(milliseconds), shell=True)


def jump_pixel(pixels):
    print(pixels)
    milliseconds = pixels * MS_PER_PIX
    press_screen(round(milliseconds))
