#! python
# coding: utf-8
__author__ = 'MarcoQin'

import time
import subprocess
from threading import Thread
from CPlayer import *


class Player(object):

    def __init__(self, song_data, queue=None, ui_object=None):
        self._pause = False
        self._is_playing = False
        self._time_pos = 0
        self._file_info = {}
        self.song_data = song_data  # model.Song
        self.player = None
        self.queue = queue
        self.ui_main = ui_object
        self.watch_dog_stated = False

    def start(self, uri):
        if not self.watch_dog_stated:
            Thread(target=self.watch_dog).start()
            self.watch_dog_stated = True
        cp_load_file_py(uri.encode('utf-8'))
        self._is_playing = True

    def play(self):
        current_song = self.song_data.current_song
        if self.is_alive:
            if self._pause:
                self.pause()
            else:
                self.load_file(current_song.path)
        else:
            self.start(current_song.path)

    def load_file(self, uri):
        cp_load_file_py(uri.encode('utf-8'))

    def set_volume(self, vol):
        if self.is_alive:
            cp_set_volume_py(vol)

    def double_select_song(self, uri):
        self._push_song_to_play_queue(uri)

    def _push_song_to_play_queue(self, uri):
        print self.is_alive
        if self.is_alive:
            self.load_file(uri)
        else:
            self.start(uri)

    def next(self):
        song = self.song_data.next_song
        self._push_song_to_play_queue(song.path)

    def previous(self):
        song = self.song_data.previous_song
        self._push_song_to_play_queue(song.path)

    def pause(self):
        if self.is_alive:
            self._pause = not self._pause
            cp_pause_audio_py()

    def stop(self):
        if self.is_alive:
            cp_stop_audio_py()

    def seek(self, seconds):
        if self.is_alive:
            cp_seek_audio_by_sec_py(seconds)

    @property
    def time_pos(self):
        return cp_get_current_time_pos_py()

    @property
    def total_length(self):
        return cp_get_time_length_py()

    @property
    def is_alive(self):
        return cp_is_alive_py()

    @property
    def file_info(self):
        """
        the file info
        """
        base = {
            'length': cp_get_time_length_py(),
            'name': '',
            'album': '',
            'artist': '',
            'genre': '',
            'title': '',
            'date': ''
        }
        info = self.song_data.get_meta_data()
        base.update(info)
        return base

    def free_player(self):
        cp_free_player_py()

    def watch_dog(self):
        while(1):
            if self.ui_main.quit:
                break
            if not cp_is_stopping_py():
                time.sleep(1)
                continue
            if self.ui_main.wasPlaying:
                self.queue.put('stopping')
                time.sleep(3)

if __name__ == '__main__':
    #  a = subprocess.Popen(['mplayer', '-slave', '-nolirc', '-quiet', '-softvol', "/home/marcoqin/marco/audiodump.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    #  print a
    #  def b():
        #  a.wait()
    #  Thread(target=b).start()
    uri = raw_input('please input file path: ')
    #  Player().play("/home/marcoqin/音乐/小森きり - 砕月～イノチ～.flac")
    player = Player()
    while True:
        cmd = raw_input('input cmd: ')
        if cmd == 'start':
            player.play(uri)
        else:
            result = getattr(player, cmd)
            if callable(result):
                print result()
            else:
                print result
