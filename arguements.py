# 下列是根据1920*1080分辨率预设参数,可根据实际分辨率调整
CROP_X_L = 140  # 裁剪原始截图时,左侧边X值
CROP_X_R = 1025  # 裁剪原始截图时,右侧边X值
CROP_Y_U = 700  # 裁剪原始截图时,上侧边Y值
CROP_Y_D = 1200  # 裁剪原始截图时,下侧边Y值
CIRCLE_R = 30  # 模型头部半径
PLAYER_HEIGHT = 200  # 模型头顶到底座像素高度
DIVIDE_X = 10  # 划分图形区域的最小X值,推荐值大于2
DIVIDE_Y = 5  # 划分图形区域的最小Y值,推荐值大于2
MIN_POINTS_LIMIT = 20  # 有效图形区域的最小坐标点数量限制,小于该值视为无效区域
MS_PER_PIX = 1.36  # 跳跃1px距离需要长按约1.4ms(粗率计算)

# 下列是用于geometry_data_verify方法的相关参数,与图形识别容差有关。
SAMPLE_SIZE = 15  # 根据坐标点识别图形时,取样的样本容量
TOLERANCE = 0.05  # 样本值与标准值的最大偏差率
EXCLUSION = 1  # 排除异常值个数

MIN_GRAYSCALE_LIMIT = 5  # 最小灰度限制,用于过滤掉图形边界以外的点,推荐值5
TIME_INTERVAL = 1.8  # 两次跳跃的间隔时间(秒),推荐不小于1.5,避免模型落地前就开始下一次识别

ADB_PATH = "/home/apps/adb"  # ADB调用路径

# DEBUG调试参数
DEBUG_MODE = False  # 是否开启DEBUG模式,开启的话将保存原截图及处理后图片
PIC_DIR = "./pic"  # 图片保存路径
PIC_NAME = "1514818335.png"  # 使用None值,则通过adb获取截图; 指定图片名称,则从PIC_DIR下查找图片文件(仅DEBUG模式)
WHITE_GRAYSCALE = 255  # 纯白灰度值
BLACK_GRAYSCALE = 0  # 纯黑灰度值
