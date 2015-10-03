# coding: utf-8
from db import DB


class Song(object):

    def __init__(self, song_id=None):
        self.db = DB()
        self.current_song_id = song_id  # current song

    def _get_current_song(self):
        if self.current_song_id:
            song = self.db.get('select * from songs where id = {0}'.format(self.current_song_id))
        else:
            sql = 'select * from songs where is_playing = 1 limit 1'
            song = self.db.get(sql)
            if song:
                self.current_song_id = song.id
            else:
                sql = 'select * from songs limit 1'
                song = self.db.get(sql)
                if song:
                    self.current_song_id = song.id
                    self.set_playing(song.id)
        return song

    def _get_song(self, next=True):
        if not self.current_song_id:
            song = self.db.get('select * from songs limit 1')
            if song:
                self.unset_playing(self.current_song_id)
                self.current_song_id = song.id
        else:
            sql = 'select * from songs where id > {0} limit 1'.format(self.current_song_id)
            if not next:  # previous
                sql = 'select * from songs where id < {0} limit 1'.format(self.current_song_id)
            song = self.db.get(sql)
            if not song:
                sql = 'select * from songs limit 1'
                if not next:
                    sql = 'select * from songs order by id desc limit 1'
                song = self.db.get(sql)
            if song:
                self.current_song_id = song.id
        if song:
            self.set_playing(song.id)
        return song

    @property
    def current_song(self):
        song = self._get_current_song()
        return song

    @property
    def next_song(self):
        song = self._get_song(next=True)
        return song

    @property
    def previous_song(self):
        song = self._get_song(next=False)
        return song

    def set_playing(self, song_id):
        sql = 'update songs set is_playing = 1 where id = {0}'.format(song_id)
        self.db.execute(sql)

    def unset_playing(self, song_id):
        sql = 'update songs set is_playing = 0 where id = {0}'.format(song_id)
        self.db.execute(sql)
