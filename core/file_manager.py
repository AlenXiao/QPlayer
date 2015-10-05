# coding: utf-8
from db import DB


class FileManager(object):

    def __init__(self):
        self.db = DB()

    def add_files(self, files):
        sql = 'insert into songs (name, path) values '
        for file in files:
            file_name = file.rsplit('/')[-1]
            sql += '("{0}", "{1}"),'.format(file_name, file)
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
