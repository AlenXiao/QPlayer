# coding: utf-8
__author__ = 'MarcoQin'

import os
import sys
import time
import subprocess
from threading import Thread
import Queue

class Player(object):

    def __init__(self, queue):
        self.queue = queue
        self.play_args = [
            'mplayer',
            '-slave',
            '-nolirc',          # Get rid of a warning
            '-quiet',           # Cannot use really-quiet because of get_* queries
            '-softvol',         # Avoid using hardware (global) volume
            'uri'
        ]
        self._pause = False
        self._is_playing = False
        self._time_pos = 0
        self._file_info = {}

    def play(self, uri):
        uri = self.queue.get()
        self.play_args[-1] = uri
        self.player = subprocess.Popen(self.play_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        Thread(target=self.watch_dog).start()
        self._is_playing = True

    def next(self):
        uri = self.queue.get()
        self._send_command('loadfile "{0}"'.format(uri))

    def pause(self):
        self._pause = not self._pause
        self._send_command('pause')

    def quit(self):
        if not self.is_alive:
            return
        self._send_command('stop')

    @property
    def time_pos(self):
        if self.is_alive:
            if not self._pause:
                time_pos = self._send_command('get_time_pos', 'ANS_TIME_POSITION')
                self._time_pos = int(float(time_pos))
            return self._time_pos
        return 0

    @property
    def is_alive(self):
        if self.player is None:
            return False
        return self.player.poll() is None

    @property
    def file_info(self):
        """
        the file info
        """
        base = {
                'get_time_length': ('ANS_LENGTH', 'length'),
                'get_file_name': ('ANS_FILENAME', 'file_name'),
                'get_meta_album': ('ANS_META_ALBUM', 'album'),
                'get_meta_artist': ('ANS_META_ARTIST', 'artist'),
                'get_meta_comment': ('ANS_META_COMMENT', 'comment'),
                'get_meta_genre': ('ANS_META_GENRE', 'genre'),
                'get_meta_title': ('ANS_META_TITLE', 'title'),
                'get_meta_year': ('ANS_META_YEAR', 'year')
                }
        if not self.is_alive:
            return
        if not self._pause:
            for k, v in base.items():
                self._file_info[v[1]] = self._send_command(k, v[0])
        return self._file_info

    def _send_command(self, cmd, extract_string=None):
        """
        cmd: command need to execute
        extract_string: if extract_string is not None, return the tring extracted from
                        stdout
        """
        cmd += '\n'
        try:
            self.player.stdin.write(cmd)
        except (TypeError, UnicodeEncodeError):
            self.player.stdin.write(cmd.encode('utf-8'))
        time.sleep(0.1)
        if not extract_string:
            return
        #  for line in self.player.stdout:
            #  if extract_string in line:
                #  return line.split('=')[1].strip()

        while 1:
            try:
                output = self.player.stdout.readline().rstrip()
            except IOError:
                return
            if extract_string in output:
                return output.split('=')[1].strip()


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
    queue = Queue.Queue(maxsize=1000)
    for root,dirs,files in os.walk(uri):
        for song in files:
            queue.put('{0}{1}'.format(root, song))
    player = Player(queue)
    while 1:
        cmd = raw_input('input cmd: ')
        if cmd == 'start':
            player.play(uri)
        else:
            result = getattr(player, cmd)
            if callable(result):
                print result()
            else:
                print result
