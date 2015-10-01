# coding: utf-8
__author__ = 'MarcoQin'

import os
import sys
import time
import subprocess
from threading import Thread

class Player(object):

    def __init__(self):
        self.default_args = [
            'mplayer',
            '-slave',
            '-nolirc',          # Get rid of a warning
            '-quiet',           # Cannot use really-quiet because of get_* queries
            '-softvol',         # Avoid using hardware (global) volume
            'uri'
        ]

    def play(self, uri):
        self.default_args[-1] = '"%s"'%uri
        # print ' '.join(self.default_args)
        print ' '.join(self.default_args)
        #  subprocess.Popen(' '.join(self.default_args), stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        subprocess.Popen('mplayer -slave -nolirc -quiet -softvol "/home/marcoqin/audiodump.wav"', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        # self.core = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        # self.core.stdin.write('\n')
        # time.sleep(0.1)
        # self.core.wait()
        # Thread(target=self.core.wait).start()

if __name__ == '__main__':
    os.chdir(os.path.abspath('/'))
    print os.path.abspath('/')
    #  a = subprocess.Popen('mplayer -slave -nolirc -quiet -softvol "/home/marcoqin/marco/audiodump.wav"', shell=True) # this can work
    a = subprocess.Popen(['mplayer', '-slave', '-nolirc', '-quiet', '-softvol', "/home/marcoqin/marco/audiodump.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    print a
    def b():
        a.wait()
    Thread(target=b).start()
    #  Player().play("/home/marcoqin/音乐/小森きり - 砕月～イノチ～.flac")
