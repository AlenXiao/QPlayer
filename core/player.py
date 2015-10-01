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
        self.default_args[-1] = uri
        self.player = subprocess.Popen(self.default_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        Thread(target=self.watch_dog).start()
        while 1:
            args = raw_input('input cmd--> ')
            self.player.stdin.write(args+'\n')
            while 1:
                try:
                    result = self.player.stdout.readline()
                except IOError:
                    break
                if 'ANS_FILENAME' in result:
                    print result
                    break

    def watch_dog(self):
        self.player.wait()

if __name__ == '__main__':
    #  a = subprocess.Popen(['mplayer', '-slave', '-nolirc', '-quiet', '-softvol', "/home/marcoqin/marco/audiodump.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    #  print a
    #  def b():
        #  a.wait()
    #  Thread(target=b).start()
    uri = raw_input('please input file path: ')
    #  Player().play("/home/marcoqin/音乐/小森きり - 砕月～イノチ～.flac")
    Player().play(uri)
