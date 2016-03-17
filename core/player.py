# coding: utf-8
__author__ = 'MarcoQin'

import time
import subprocess
from threading import Thread
from CPlayer import *


class Player(object):

    def __init__(self, song_data, queue=None, ui_object=None):
        self.play_args = [
            'mplayer',
            '-slave',
            '-msglevel',  # message level: ignore all we don't want
            'all=-1:global=5',
            '-nolirc',          # Get rid of a warning
            '-quiet',           # Cannot use really-quiet because of get_* queries
            '-softvol',         # Avoid using hardware (global) volume
        ]
        self._pause = False
        self._is_playing = False
        self._time_pos = 0
        self._file_info = {}
        self.song_data = song_data  # model.Song
        self.player = None
        self.queue = queue
        self.ui_main = ui_object

    def start(self, uri):
        """
        'cp_free_player_py',
        'cp_get_current_time_pos_py',
        'cp_get_time_length_py',
        'cp_is_stopping_py',
        'cp_load_file_py',
        'cp_pause_audio_py',
        'cp_stop_audio_py'
        """
        #  args = self.play_args + [uri]
        #  self.player = subprocess.Popen(
            #  args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        #  Thread(target=self.watch_dog).start()
        cp_load_file_py(uri)
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
        #  self._send_command('loadfile "{0}"'.format(uri.encode('utf-8')))
        cp_load_file_py(uri)

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
        #  self._pause = not self._pause
        #  self._send_command('pause')
        cp_pause_audio_py()

    def stop(self):
        #  if self.is_alive:
            #  self._send_command('stop')
        cp_stop_audio_py()

    def seek(self, seconds):
        if self.is_alive:
            self._send_command('seek {0}'.format(seconds))

    @property
    def time_pos(self):
        #  if self.is_alive:
            #  if not self._pause:
                #  time_pos = self._send_command(
                    #  'get_time_pos', 'ANS_TIME_POSITION')
                #  self._time_pos = int(float(time_pos))
            #  return self._time_pos
        #  return 0
        return cp_get_current_time_pos_py()

    @property
    def total_length(self):
        return cp_get_time_length_py()

    @property
    def is_alive(self):
        #  if self.player is None:
            #  return False
        #  return self.player.poll() is None
        return True

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
            #  'get_meta_comment': ('ANS_META_COMMENT', 'comment'),
            'get_meta_genre': ('ANS_META_GENRE', 'genre'),
            'get_meta_title': ('ANS_META_TITLE', 'title'),
            #  'get_meta_year': ('ANS_META_YEAR', 'year')
        }
        #  if not self.is_alive:
            #  return
        #  if not self._pause:
            #  for k, v in base.items():
                #  self._file_info[v[1]] = self._send_command(k, v[0])
        for k, v in base.items():
            self._file_info[v[1]] = 'TEST'
        self._file_info['length'] = cp_get_time_length_py()
        return self._file_info

    def free_player(self):
        cp_free_player_py()

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
        for line in iter(self.player.stdout.readline, ''):
            if extract_string in line:
                return line.split('=')[1].strip()

        #  while 1:
            #  try:
                #  output = self.player.stdout.readline().rstrip()
            #  except IOError:
                #  return
            #  if extract_string in output:
                #  return output.split('=')[1].strip()

    def watch_dog(self):
        return_code = self.player.wait()
        print return_code
        if return_code == 0:
            if self.ui_main.wasPlaying:
                self.queue.put('stopping')

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
