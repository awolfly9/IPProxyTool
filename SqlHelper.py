#-*- coding: utf-8 -*-
import logging
import random
import sqlite3
import threading

from Proxy import Proxy
from Singleton import Singleton
lock = threading.Lock()


class SqlHelper(Singleton):
    def __init__(self):
        self.database_name = 'ipproxy.db'
        self.table_name = 'ipproxy'

        self.database = None
        self.cursor = None

        self.init()
        print('Sqlhelper __init__')

    def init(self):
        self.create_database()
        self.create_table()

    def create_database(self):
        try:
            lock.acquire(True)

            self.database = sqlite3.connect(self.database_name, check_same_thread = False)
            self.cursor = self.database.cursor()

            lock.release()
        except Exception, e:
            lock.release()
            logging.error('SqlHelper create_database exception:%s' % e)
            print('SqlHelper create_database exception:%s' % e)


    def create_table(self):
        try:
            lock.acquire(True)

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS %s (
                                               ip TEXT NOT NULL,
                                               port TEXT NOT NULL,
                                               country TEXT NOT NULL,
                                               anonymity TEXT NOT NULL,
                                               https TEXT NOT NULL,
                                               speed TEXT NOT NULL)''' % self.table_name)

            self.database.commit()

            lock.release()
        except Exception, e:
            lock.release()
            logging.error('sql helper create_table exception:%s' % str(e))
            print('sql helper create_table exception:%s' % str(e))

    def insert_data(self, proxy):
        try:
            lock.acquire(True)

            data = [proxy.ip, proxy.port, proxy.country, proxy.anonymity, proxy.https, proxy.speed]

            logging.info('insert data:%s' % str(data))
            print('insert data:%s' % str(data))

            self.cursor.execute("INSERT INTO %s VALUES (?,?,?,?,?,?)" % self.table_name, data)
            self.database.commit()

            lock.release()
        except Exception, e:
            lock.release()
            logging.warning('sql helper insert_data exception:%s' % str(e))
            print('sql helper insert_data exception:%s' % str(e))


    def batch_insert_data(self, proxys):
        try:
            lock.acquire(True)

            for proxy in proxys:
                data = [proxy.ip, proxy.port, proxy.country, proxy.anonymity, proxy.https, proxy.speed]
                self.cursor.execute("INSERT INTO %s VALUES (?,?,?,?,?,?)" % self.table_name, data)

            self.database.commit()

            lock.release()
        except Exception, e:
            lock.release()
            logging.warning('sql helper batch_insert_data exception:%s' % str(e))
            print('sql helper batch_insert_data exception:%s' % str(e))

    def drop_table(self):
        try:
            lock.acquire(True)

            self.cursor.execute('DROP TABLE %s' % self.table_name)
            self.database.commit()

            lock.release()
        except Exception, e:
            lock.release()
            logging.warning('sql helper drop_table exception:%s' % str(e))
            print('sql helper drop_table exception:%s' % str(e))

    def select_all(self):
        try:
            lock.acquire(True)

            self.cursor.execute('SELECT * FROM %s' % self.table_name)
            result = self.cursor.fetchall()

            lock.release()
            return result
        except Exception, e:
            lock.release()
            logging.warning('sql helper select_all exception:%s' % str(e))
            print('sql helper select_all exception:%s' % str(e))
            return []

    def select_once(self):
        try:
            lock.acquire(True)

            self.cursor.execute('SELECT * FROM %s limit 1' % self.table_name)
            result = self.cursor.fetchall()

            lock.release()
            return result
        except Exception, e:
            lock.release()
            logging.warning('sql helper select_once exception:%s' % str(e))
            print('sql helper select_once exception:%s' % str(e))
            return []

    def select_count(self, count):
        try:
            lock.acquire(True)

            self.cursor.execute('SELECT * FROM %s ORDER BY speed limit %s' % (self.table_name, count))
            result = self.cursor.fetchall()
            lock.release()

            return result
        except Exception, e:
            lock.release()
            logging.warning('sql helper select_count exception:%s' % str(e))
            print('sql helper select_count exception:%s' % str(e))
            return []

    def select(self, condition, count):
        try:
            lock.acquire(True)

            if condition == '':
                command = 'SELECT DISTINCT * FROM %s ORDER BY speed ASC %s ' % (
                    self.table_name, count)
            elif count == '':
                command = 'SELECT DISTINCT * FROM %s WHERE %s ORDER BY speed' % (
                    self.table_name, condition)
            else:
                command = 'SELECT DISTINCT * FROM %s WHERE %s ORDER BY speed ASC %s ' % (
                    self.table_name, condition, count)

            logging.info('sqlhelper select commond:%s' % command)
            print('sqlhelper select commond:%s' % command)

            self.cursor.execute(command)
            result = self.cursor.fetchall()

            lock.release()
            return result
        except Exception, e:
            lock.release()
            logging.warning('sql helper select exception:%s' % str(e))
            print('sql helper select exception:%s' % str(e))
            return []

    def clear_all(self):
        try:
            lock.acquire(True)

            self.cursor.execute('DELETE FROM %s' % self.table_name)
            self.database.commit()

            lock.release()
        except Exception, e:
            lock.release()
            logging.warning('sql helper clear_all exception:%s' % str(e))
            print('sql helper clear_all exception:%s' % str(e))

    def close(self):
        try:
            lock.acquire(True)

            self.cursor.close()
            self.database.close()
        
            lock.release()
        except Exception, e:
            lock.release()
            logging.warning('sql helper close exception:%s' % str(e))
            print('sql helper close exception:%s' % str(e))

if __name__ == '__main__':
    sql = SqlHelper()
    all_rows = sql.select_all()
    for row in all_rows:
        print('proxy:%s' % str(row))
        # row[0] returns the first column in the query (name), row[1] returns email column.
        print('http://{0} : {1}'.format(row[0], row[1], ))

    #sql.clear_all()

    print('-------------------------------------')

    results = sql.cursor.execute('SELECT * FROM ipproxy WHERE country="中国" ORDER BY speed')
    for res in results:
        print('result:%s' % str(res))
        print(res[3])
        print(res[4])

    print('-------------------------------------')

    results = sql.cursor.execute('SELECT * FROM ipproxy WHERE port="8080" ORDER BY speed limit 4')
    for res in results:
        print('result:%s' % str(res))
        print(res[3])
        print(res[4])

    print('-------------------------------------')

    results = sql.select_count(10)
    for res in results:
        print('result:%s' % str(res))
        print(res[3])
        print(res[4])

    print('-------------------------------------')

    results = sql.cursor.execute('SELECT DISTINCT ip,port FROM %s WHERE %s ORDER BY speed ASC %s' % (
        sql.table_name, 'port=8080 And https="no"', 'limit 5'))
    for res in results:
        print('result:%s' % str(res))
        print(res[0])
        print(res[1])

    database = 'country="中国" And anonymity="1"'
    count = 'limit 10'

    print('-------------------------------------')
    print(database)

    results = sql.select(database, count)
    for res in results:
        print('result:%s' % str(res))
        print(res[0])
        print(res[1])

    print('-------------------------------------********')

    results = sql.select('', '')
    for res in results:
        print('result:%s' % str(res))
        print(res[0])
        print(res[1])

    print('-------------------------------------********')

    try:
        lock.acquire(True)
        print('test try')
        #print(10/0)
        lock.release()
    except Exception, e:
        print(e)
    finally:
        print('finally')
        lock.release()

        # conn = sqlite3.connect('example.db')
        # c = conn.cursor()
        #
        # 
        #     # Create table
        #     c.execute('''CREATE TABLE stocks
        #              (date TEXT, trans TEXT, symbol TEXT, qty REAL, price REAL)''')
        # except:
        #     pass
        #
        # # Insert a row of data
        # c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
        #
        # # Save (commit) the changes
        # conn.commit()
        #
        # purchases = [('2006-03-28', u'中文编码', 'IBM', 1000, 45.00),
        #              ('2006-04-05', u'这是一个中文', 'MSFT', 1000, 72.00),
        #              ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
        #              ]
        #
        # c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
        #
        # conn.commit()
        #
        # # We can also close the connection if we are done with it.
        # # Just be sure any changes have been committed or they will be lost.
        # conn.close()
        #
        # sql = SqlHelper()
        #
        # # sql.cursor.execute('''INSERT INTO ipproxy(name, phone, email, password)
        # #                   VALUES(?,?,?,?)''', (name1, phone1, email1, password1)))
        #
        # for i in range(1):
        #     p = Proxy()
        #     p.set_value('1.1.1.1', '端口', '中文', '告你', 'no', str(i))
        #     sql.insert_data(p)
        #
        #     sql.cursor.execute("INSERT INTO ipproxy VALUES ('1.1.1.1', '8080', 'china', 'anonymity', 'no', 444)")
        #     sql.database.commit()

        # purchases = [('2006-03-28', '中文支持怎么样', 'IBM', '1000', '45.00', 'djfka'),
        #              ('2006-04-05', 'BUY', 'MSFT', '1000', '72.00', 'fadfa'),
        #              ('2006-04-06', 'SELL', 'IBM', '500', '53.00', '测试这是一个中文字符串'),
        #              ]
        #
        # sql.cursor.executemany('INSERT INTO ipproxy VALUES (?,?,?,?,?,?)', purchases)
        #
        # sql.database.commit()
