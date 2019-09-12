# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from scrapy.exporters import JsonItemExporter
import pymysql
from twisted.enterprise import adbapi


class MysqlTwistedPipeline():
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            database=settings.get('MYSQL_DATABASE'),
            user=settings.get('MYSQL_USER'),
            password=settings.get('MYSQL_PASSWORD'),
            port=settings.get('MYSQL_PORT'),
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
            charset='utf8',
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, )

    def handle_error(self, failure):
        print(failure)

    def do_insert(self, cursor, item):
        data = dict(item)
        # data['front_image_url'] = data['front_image_url'][0]
        if data:
            keys = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))

            insert_sql = 'insert into {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE '.format(table=item.table, keys=keys, values=values)
            update = ', '.join(['{key}=%s'.format(key=key) for key in data])
            insert_sql += update

            cursor.execute(insert_sql, tuple(data.values())*2)