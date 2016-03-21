# coding: utf-8
import sqlite3
import itertools


class DB(object):
    """
    A torndb-like sqlite3 db model
    """

    def __init__(self):
        self.con = sqlite3.connect('playlist')
        self.con.isolation_level = None
        cur = self.con.cursor()
        sql = '''create table if not exists songs
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name varchar(255) NOT NULL,
                    path varchar(512),
                    title VARCHAR(512),
                    album VARCHAR(512),
                    artist VARCHAR(512),
                    genre VARCHAR(64),
                    track VARCHAR(64),
                    date VARCHAR(64),
                    is_playing int(2) DEFAULT 0
                )'''
        cur.execute(sql)
        cur.close()
        self.con.commit()

    def query(self, sql):
        cursor = self._cursor()
        try:
            cursor.execute(sql)
            column_names = [d[0] for d in cursor.description]
            return [Row(itertools.izip(column_names, row)) for row in cursor]
        finally:
            cursor.close()

    def get(self, sql):
        rows = self.query(sql)
        if not rows:
            return None
        else:
            return rows[0]

    def execute(self, sql):
        cursor = self._cursor()
        try:
            cursor.execute(sql)
            return cursor.lastrowid
        finally:
            cursor.close()

    def _cursor(self):
        return self.con.cursor()

    def __del__(self):
        if self.con:
            self.con.close()


class Row(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


if __name__ == '__main__':
    db = DB()
    #  db.execute('insert into songs (name, path) values ("test", "/home/test")')
    print db.query('select * from songs')
