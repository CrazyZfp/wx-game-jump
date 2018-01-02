from adb_controller import jump_pixel
import time
from image_reader import *


def jump(pic_name=None):
    img = get_img(pic_name)
    px = img.load()
    width, height = img.size

    if DEBUG_MODE:
        district_lst = get_districts_debug(px, width, height)
    else:
        district_lst = get_districts(px, width, height)

    # img.show()

    aim_co, player_co = get_coordinates(district_lst)
    distance = calculate_distance(aim_co, player_co)
    jump_pixel(distance)

    if DEBUG_MODE:
        px[aim_co[0], aim_co[1]] = WHITE_GRAYSCALE
        px[player_co[0], player_co[1]] = WHITE_GRAYSCALE
        img.save(pic_path.replace(".png", "-m.png"))
        # img.show()


if __name__ == "__main__":
    while True:
        jump(PIC_NAME)
        time.sleep(TIME_INTERVAL)
