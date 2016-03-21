# coding: utf-8
from db import DB
from CPlayer import cp_get_metadata_py


class FileManager(object):

    def __init__(self):
        self.db = DB()

    def add_files(self, files):
        #  sql = 'insert into songs (name, path) values '
        sql = 'insert into songs (name, path, title, album, artist, genre, track, date) values'
        for file in files:
            info = cp_get_metadata_py(file.decode('utf-8').encode('utf-8'))
            file_name = file.rsplit('/')[-1]
            info['name'] = file_name
            info['path'] = file
            sql += '("{name}", "{path}", "{title}", "{album}", "{artist}", "{genre}", "{track}", "{date}"),'.format(**info)
        sql = sql[:-1]
        self.db.execute(sql)

    def del_files(self, ids):
        """
        require: ids: list, tuple, set
        """
        if not ids:
            return
        query = str(tuple(ids))
        if len(ids)<2:
            query = query.replace(',', '')
        sql = 'delete from songs where id in {0}'.format(query)
        self.db.execute(sql)
