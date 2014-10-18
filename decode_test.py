# -*- coding: utf-8 -*-
"""转换mp3文件编码"""

import mp3play
import time
import os
from os.path import exists
import sys

mp3file = r'H:\musicpack\mp3\004.奈落の花 - 今日的 5年2班.mp3'
#获取现在系统的编码格式
type = sys.getfilesystemencoding()
print type
#转换成现在系统的编码
mp3file = mp3file.decode('utf-8').encode(type)
print mp3file

mp3 = mp3play.load(mp3file)

mp3.play()

#let it play for up to 30 seconds ,then stop it
time.sleep(min(10,mp3.seconds()))
mp3.stop()