# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import  pymysql

class ShanxidailyPipeline(object):
    def process_item(self, item, spider):
        conn=pymysql.connect(host='113.200.115.182',post='3306',user='root',password='!qaz@wsx',charset='utf-8')
        cusor=conn.cursor()
        cusor.execute('insert into susdepcode,susdepname values(%s,%s)',item)
        conn.commit()
        cusor.close()
        conn.close()
        return item
