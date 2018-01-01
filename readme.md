# WX-GAME-JUMP-AUTO

微信小游戏“跳一跳”的自动化脚本, 原理是简单的图像识别+[ADB](https://www.xda-developers.com/install-adb-windows-macos-linux/)

### Env
Python环境:    Python3.5<br>
Python包依赖： Pillow<br>

测试手机： Huawei Honor8 <br>
手机分辨率：   1920*1080 <br>
目前记录： 最高1863分

### Usage
可以根据运行情况,调整arguement.py中的各项参数<br>
如需保存原始截图及处理后的图片,请将DEBUG_MODE设置为True<br>
如需调试指定截图,请将DEBUG_MODE设置为True,同时设置PIC_NAME

若程序频繁因找不到模型或物块跳出(PLAYER_NOT_FOUND,BLOCK_NOT_FOUND):
* 适当调小 DIVIDE_X 和 DIVIDE_Y
* 适当增大 TOLERANCE 和 EXCLUSION

若模型经常落地：
* 调整 TIME_INTERVAL 至1.8
* 调整 MS_PER_PIX

### Problems
1.物块及阴影与模型头部有重叠时,可能会发生找不到模型的问题,导致程序跳出<br>
2.某些物块与背景色同时出现,可能影响图像识别,导致程序跳出或模型落地<br>
  (eg: **鲜黄色笑脸物块与粉白渐变色背景,浅绿色笑脸物块与灰色背景** 较大概率落地)<br>
3.模型触发音乐盒物块,产生的音符有几率影响模型头部识别<br>
