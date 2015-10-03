# coding: utf-8
from db import DB


class FileManager(object):

    def __init__(self):
        self.db = DB()

    def add_files(self, files):
        for file in files:
            file_name = file.rsplit('/')[-1]
            sql = 'insert into songs (name, path) values ("{0}", "{1}")'.format(file_name, file)
            self.db.execute(sql)

