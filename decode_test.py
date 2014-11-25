# -*- coding: utf-8 -*-
"""ת��mp3�ļ�����"""

import mp3play
import time
import os
from os.path import exists
import sys

#mp3file = r'H:\musicpack\mp3\004.����λ� - ���յ� 5��2��.mp3'
#��ȡ����ϵͳ�ı����ʽ
type = sys.getfilesystemencoding()
print type
#ת��������ϵͳ�ı���
#mp3file = mp3file.decode('utf-8').encode(type)
#print mp3file

#mp3 = mp3play.load(mp3file)

#mp3.play()

#let it play for up to 30 seconds ,then stop it
#time.sleep(min(10,mp3.seconds()))
#mp3.stop()