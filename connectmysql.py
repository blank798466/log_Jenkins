# coding=utf-8
import MySQLdb
from DBUtils.PooledDB import PooledDB

pool = PooledDB(MySQLdb, 5,
                host='192.168.11.248',
                port=10086,
                user='root',
                passwd='whu12345',
                db='logs')
conn = pool.connection()
cursor = conn.cursor()

sql_1 = "select * from logs_pipeline"

try:
    cursor.execute(sql_1)
    print cursor.fetchall()

    conn.commit()

except Exception as e:
    print e
    conn.rollback()

cursor.close()
conn.close()
