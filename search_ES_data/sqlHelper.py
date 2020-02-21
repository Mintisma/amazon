import pymysql

# from settings import USER, HOST, DB, PASSWORD
from settings import db


class Sqlhelper:
    def __init__(self):
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(db['HOST'], port=3306, user=db['USER'], password=db['PASSWORD'], db=db['NAME'], charset='utf8')
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def get_list(self, sql, args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    def get_one(self, sql, args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    def modify(self, sql, args):
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
        except pymysql.err.InternalError as e:
            print(e)
        return self.cursor.lastrowid

    def modify_many(self, sql, args):
        self.cursor.executemany(sql, args)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()