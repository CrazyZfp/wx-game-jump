from PIL import Image
from math import floor, sqrt
from adb_controller import get_cap_bytes
from arguements import *

if DEBUG_MODE:
    from adb_controller import get_cap_path

    pic_path = ''


def current_district(district_lst):
    if len(district_lst) > 0:
        return district_lst[-1]
    else:
        return new_district(district_lst)


def new_district(district_lst):
    district_lst.append({"edge_point_list": [], "vertex_list": [], "vertex_y": 10000})
    return district_lst[-1]


def judge_district(cur_edge_point, last_edge_point):
    # 如果当前点的x或y坐标与上一个点的x或y坐标差值大于20,则将该点视为新区域的点
    if abs(last_edge_point[0] - cur_edge_point[0]) > DIVIDE_X or abs(last_edge_point[1] - cur_edge_point[1]) > DIVIDE_Y:
        return True
    else:
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


# def get_absolute_coordinate(r_co):
#     return r_co[0] + 140, r_co[1] + 700


def get_vertex_x(vertex_list):
    """获取顶点x坐标"""
    return sum(it[0] for it in vertex_list) / len(vertex_list)


def calculate_distance(p1, p2):
    """
    计算两坐标点间距
    """
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def geometry_data_verify(data_list, std_data=None, tolerance=TOLERANCE):
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

    for dif in diff_list[:-EXCLUSION]:  # 排除误差最大的值
        if dif > std_float:
            return False
    return True


def circle_recognize(p_list):
    """根据坐标list判断是否是圆（模型头部）"""

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
    """ 获取用户当前坐标(相对于裁剪后的图片)"""
    vertex_list = player_district["vertex_list"]
    vertex = (get_vertex_x(vertex_list), player_district["vertex_y"])
    p_list = quarter_filter(player_district['edge_point_list'], vertex)
    if len(p_list) > SAMPLE_SIZE and circle_recognize(p_list):
        return vertex[0], vertex[1] + PLAYER_HEIGHT
    else:
        return None


def quarter_filter(edge_p_list, vertex):
    """在 边界坐标列表 中筛选出目标图形（菱形或椭圆或圆）右上方约1/4边界的坐标点集合"""
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
    """
    获取落点坐标
    :param aim_district: 落点物块的图形区域
    :return: 落点坐标
    """
    vertex = (get_vertex_x(aim_district["vertex_list"]), aim_district["vertex_y"])
    edge_p_list = aim_district["edge_point_list"]

    p_list = quarter_filter(edge_p_list, vertex)
    if len(p_list) <= 1:
        raise Exception("BLOCK_NOT_FOUND")
    aim_r_co = (p_list[0][0], p_list[-1][1])
    return aim_r_co


def get_img(pic_name=None):
    """
    从数据流或文件获取Image对象，并做简单处理
    :param pic_name: 截图名称
    :return: 原截图经灰度化,FIND_EDGES滤镜,裁剪后的Image对象
    """
    if DEBUG_MODE:
        global pic_path
        if pic_name is None:
            pic_path = get_cap_path()
        else:
            pic_path = '{pic_dir}/{pic_name}'.format(pic_dir=PIC_DIR, pic_name=pic_name)
        img = Image.open(pic_path)
    else:
        img = Image.open(get_cap_bytes())

    # img = img.convert("L")
    # img = img.filter(ImageFilter.FIND_EDGES)
    return img.crop((CROP_X_L, CROP_Y_U, CROP_X_R, CROP_Y_D))


def get_districts_debug(px, img_width, img_height):
    """
    get_districts的DEBUG模式
    该模式下将遍历整个px，并将未被收入districts的点设置为纯黑，收入的点设置为纯白，便于debug执行结果

    :param px: 像素点阵
    :param img_width: 图片宽度
    :param img_height: 图片高度
    :return: 图形区域列表
    """
    district_lst = []
    last_edge_point = (0, 0)
    bg_rgb = px[0, 0]

    for wi in range(img_width):
        hi = 0
        flag = True
        while hi < img_height:
            cur_point = (wi, hi)
            cur_rgb = px[wi, hi]
            if flag and (abs(cur_rgb[0] - bg_rgb[0]) > MIN_RGB_TOLERANCE or abs(
                        cur_rgb[1] - bg_rgb[1]) > MIN_RGB_TOLERANCE or abs(
                    cur_rgb[2] - bg_rgb[2]) > MIN_RGB_TOLERANCE):
                flag = False
                px[wi, hi] = (WHITE_GRAYSCALE, WHITE_GRAYSCALE, WHITE_GRAYSCALE)

                if judge_district(cur_point, last_edge_point):
                    district = new_district(district_lst)
                else:
                    district = current_district(district_lst)
                add_edge_point(district, cur_point)
                last_edge_point = cur_point
            else:
                px[wi, hi] = (BLACK_GRAYSCALE, BLACK_GRAYSCALE, BLACK_GRAYSCALE)
            hi += 1
    return district_lst


def get_districts(px, img_width, img_height):
    """
    根据图片像素点灰度值，查找图形边界坐标点，并按一定规则将获得的坐标点划分图形区域
    :param px: 像素点阵
    :param img_width: 图片宽度
    :param img_height: 图片高度
    :return: 图形区域列表
    """
    district_lst = []
    last_edge_point = (0, 0)
    bg_rgb = px[0, 0]
    for wi in range(img_width):
        hi = 0
        while hi < img_height:
            cur_point = (wi, hi)
            cur_rgb = px[wi, hi]
            # if px[wi, hi] >= MIN_GRAYSCALE_LIMIT:
            if abs(cur_rgb[0] - bg_rgb[0]) > MIN_RGB_TOLERANCE or abs(
                            cur_rgb[1] - bg_rgb[1]) > MIN_RGB_TOLERANCE or abs(
                        cur_rgb[2] - bg_rgb[2]) > MIN_RGB_TOLERANCE:
                if judge_district(cur_point, last_edge_point):
                    district = new_district(district_lst)
                else:
                    district = current_district(district_lst)
                add_edge_point(district, cur_point)
                last_edge_point = cur_point
                break
            hi += 1
    return district_lst


def get_coordinates(district_lst):
    """
    由district_lst获取起点坐标和终点坐标
    :param district_lst: 区域列表
    :return: 终点坐标，起点坐标
    """
    district_lst_filtered = [x for x in district_lst if len(x["edge_point_list"]) >= MIN_POINTS_LIMIT]
    district_lst_filtered.sort(key=lambda x: x['vertex_y'])
    # district_lst_filtered[0] 可能是目标物块的边界，也可能是玩家模型头部边界
    # 若district_lst_filtered[0] 不是目标物块边界，则district_lst_filtered[1]一定是目标块边界
    player_co = get_player_coordinate(district_lst_filtered[0])
    if player_co is None:
        aim_co = get_aim_coordinate(district_lst_filtered[0])
        for lst in district_lst_filtered[1:]:
            player_co = get_player_coordinate(lst)
            if player_co is not None:
                break
        if player_co is None:
            raise Exception("PLAYER_NOT_FOUND")
    else:
        aim_co = get_aim_coordinate(district_lst_filtered[1])
    return aim_co, player_co
