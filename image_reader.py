from PIL import Image, ImageFilter
from math import floor, sqrt
from adb_controller import get_cap_bytes, jump_pixel, get_cap_path
import time

PLAYER_HEIGHT = 200
SAMPLE_SIZE = 15
CIRCLE_R = 30
MODE = 'DEBUG1'

district_lst = []
last_edge_point = (0, 0)


def current_district():
    if len(district_lst) > 0:
        return district_lst[-1]
    else:
        return new_district()


def new_district():
    district_lst.append({"edge_point_list": [], "vertex_list": [], "vertex_y": 1000})
    return district_lst[-1]


def judge_district(cur_edge_point):
    # 如果当前点的x或y坐标与上一个点的x或y坐标差值大于20,则将该点视为新区域的点
    if abs(last_edge_point[0] - cur_edge_point[0]) > 20 or abs(last_edge_point[1] - cur_edge_point[1]) > 30:
        global last_edge_point
        last_edge_point = cur_edge_point
        return True
    else:
        global last_edge_point
        last_edge_point = cur_edge_point
        return False


def add_edge_point(p_district, point):
    p_district["edge_point_list"].append(point)
    vertex_y = p_district["vertex_y"]
    # 判断新点的y坐标是否小于区域当前顶点的y坐标
    # 若是，则将该区域顶点列表更新为仅point
    # 若相同，则将point加入该区域的顶点列表
    if point[1] < vertex_y:
        p_district["vertex_y"] = point[1]
        p_district["vertex_list"] = [point]
    elif point[1] == vertex_y:
        p_district["vertex_list"].append(point)


def get_absolute_coordinate(r_co):
    return r_co[0] + 140, r_co[1] + 700


def get_vertex_x(vertex_list):
    return sum(it[0] for it in vertex_list) / len(vertex_list)


def calculate_distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def geometry_data_verify(data_list, std_data=None, tolerance=0.05):
    """判断数据集中的数据是否足够接近标准值
       std_data: 标准值. 若未指定，则取data_list中位数做标准值
       tolerance: 误差百分比(默认5%)
    """
    if std_data is not None:
        data_list.sort()
        std_data = data_list[floor(SAMPLE_SIZE / 2)]  # 取中位数作为标准值
    std_float = std_data * tolerance  # 合理的误差范围

    diff_list = []  # data_list中各个数值与std_data的差值的绝对值集合

    for d in data_list:
        diff_list.append(abs(d - std_data))
    diff_list.sort()

    for dif in diff_list[:-1]:  # 排除误差最大的值
        if dif > std_float:
            return False
    return True


def circle_recognize(p_list):
    "根据坐标list判断是否是圆（玩家模型头部）"

    vertex = p_list[0]
    center = (vertex[0], vertex[1] + CIRCLE_R)

    p_amount = len(p_list)
    step = 1  # 获取样本点的步长
    if p_amount > SAMPLE_SIZE:
        step = p_amount / SAMPLE_SIZE
    r_list = []
    for i in range(1, SAMPLE_SIZE):
        r_list.append(round(calculate_distance(p_list[floor(i * step)], center), 1))
    return geometry_data_verify(data_list=r_list, std_data=CIRCLE_R)


def get_player_coordinate(player_district):
    " 获取用户当前坐标(相对于裁剪后的图片)"
    vertex_list = player_district["vertex_list"]
    vertex = (get_vertex_x(vertex_list), player_district["vertex_y"])
    p_list = quarter_filter(player_district['edge_point_list'], vertex)
    # p_list = player_district['edge_point_list']
    if len(p_list) > SAMPLE_SIZE and circle_recognize(p_list):
        return vertex[0], vertex[1] + PLAYER_HEIGHT
    else:
        return None
        # return get_absolute_coordinate(player_r_co)


def quarter_filter(edge_p_list, vertex):
    "在 边界坐标列表 中筛选出目标图形（菱形或椭圆）右上方边界的点集合"
    quarter_p_list = []
    last_y = 0
    for i, p in enumerate(edge_p_list):
        if p[0] >= vertex[0] and p[1] >= last_y:
            quarter_p_list.append(p)
        last_y = p[1]
    return quarter_p_list


# def calculate_slop(origin, point):
#     return round((point[1] - origin[1]) / (point[0] - origin[0]), 2)

def get_aim_coordinate(aim_district):
    vertex = (get_vertex_x(aim_district["vertex_list"]), aim_district["vertex_y"])
    edge_p_list = aim_district["edge_point_list"]

    # 筛选出菱形右上斜边坐标点list
    p_list = quarter_filter(edge_p_list, vertex)
    aim_r_co = (p_list[0][0], p_list[-1][1])
    return aim_r_co
    # return get_absolute_coordinate(aim_r_co)

    # 在p_list中 等距离 取10个点(含index=0的点)，计算其到顶点vertex（即p_list[0])的斜率是否接近
    # 接近，可知p_list中坐标构成的是直线
    # p_amount = len(p_list)
    # step = 1  # 获取样本点的步长
    # if p_amount > 10:
    #     step = p_amount / 10
    # slop_list = []
    # for i in range(start=1, stop=9, step=1):
    #     slop_list.append(calculate_slop(p_list[0], p_list[floor(i * step)]))
    #
    # if beenline_recognize(slop_list):
    #     aim_r_co = (p_list[0][0], p_list[-1][1])
    #     return get_absolute_coordinate(aim_r_co)
    # else:


def jump():
    pic_path = ''

    if MODE == 'DEBUG':
        # pic_path = '/home/zfp/Coding/Projects/wx-game-controller/pic/1514785062.png'
        pic_path = get_cap_path()
        img = Image.open(pic_path)
    else:
        img = Image.open(get_cap_bytes())

    img = img.convert("L")

    img = img.filter(ImageFilter.FIND_EDGES)
    img = img.crop((140, 700, 1025, 1200))

    w, h = img.size

    px = img.load()
    for wi in range(w):
        hi = 0
        flag = True
        while hi < h:
            if px[wi, hi] > 4 and flag:
                flag = False
                px[wi, hi] = 255
                cur_point = (wi, hi)

                if judge_district(cur_point):
                    district = new_district()
                else:
                    district = current_district()
                add_edge_point(district, cur_point)
            else:
                px[wi, hi] = 0
            hi += 1

    district_lst_filtered = [x for x in district_lst if len(x["edge_point_list"]) > 10]
    district_lst_filtered.sort(key=lambda x: x['vertex_y'])

    # district_lst_filtered[0] 可能是目标块的边界，也可能是玩家模型头部边界
    # 若district_lst_filtered[0] 不是目标块边界，则district_lst_filtered[1]一定是目标块边界
    player_co = get_player_coordinate(district_lst_filtered[0])
    if player_co == None:
        aim_co = get_aim_coordinate(district_lst_filtered[0])
        for lst in district_lst_filtered[1:]:
            player_co = get_player_coordinate(lst)
            if player_co != None:
                break
        if player_co == None:
            raise Exception("PLAYER_NOT_FOUND")
    else:
        aim_co = get_aim_coordinate(district_lst_filtered[1])

    distance = calculate_distance(aim_co, player_co)

    jump_pixel(distance)


    if MODE == 'DEBUG':
        px[aim_co[0], aim_co[1]] = 255
        px[player_co[0], player_co[1]] = 255
        img.save(pic_path.replace(".", "-m."))
        # img.show()


if __name__ == "__main__":
    while (True):
        jump()
        district_lst.clear()
        last_edge_point = (0, 0)
        time.sleep(1.5)
