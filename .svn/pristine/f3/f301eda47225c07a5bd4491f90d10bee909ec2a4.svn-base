import pymysql

class my_sql(object):
    def __init__(self):
        self.db = pymysql.connect(host='18.191.190.29',port=3306,user='gift',passwd='123456', db='test', charset='utf8')
        self.cursor = self.db.cursor()

    def select(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def orther(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except:
            return False

if __name__ == "__main__":
    my = my_sql()
    update_time = my.select('select update_time from time_limit where ip = "%s"' % '127.0.0.1')
    print(update_time)
