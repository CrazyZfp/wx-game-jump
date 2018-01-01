#WX-GAME-JUMP-AUTO

微信小游戏“跳一跳”的自动化脚本, 原理是简单的图像识别+[ADB](https://www.xda-developers.com/install-adb-windows-macos-linux/)

###Env
Python环境:    Python3.5<br>
Python包依赖： Pillow<br>

测试手机： Huawei Honor8 <br>
手机分辨率：   1920*1080 <br>
目前记录： 最高737分, 400~500分段较多

###Usage
可以根据运行情况,调整arguement.py中的各项参数
如需保存原始截图及处理后的图片,请将DEBUG_MODE设置为True
如需调试指定截图,请将DEBUG_MODE设置为True,同时设置PIC_NAME

###Problems
1.物块及阴影对模型头部有遮挡时,可能会发生找不到模型的问题,导致程序中断<br>
2.某些物块与背景色同时出现,可能产生测距问题,导致模型落地(eg:鲜黄色物块与粉白渐变色背景,浅绿色物块与灰色背景..)<br>
3.模型触发音乐盒物块,产生的音符可能影响模型头部识别<br>
4.屏幕长按时间与跳跃距离比值不够精确,实际落点和计划落点可能会有偏差