import pymysql
import time
from threading import Thread, Event

conn = pymysql.connect(host="123.56.252.172", user="ywm", password="ywm5842154", database="student")

INSERT_EVENT = Event()

class OpenDB:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()
    

def insert_data():
    global conn, INSERT_EVENT, flag
    sql = "insert into test(name, age) values('%s', %s)" % ("xiaoming", 23)
    with OpenDB(conn) as f:
        while True:
            INSERT_EVENT.wait()
            f.execute(sql)
            conn.commit()
            time.sleep(2)

def main():
    global INSERT_EVENT
    choice = input("开始/停止：")
    if choice == 'y':
        INSERT_EVENT.set()
        return True
    
    if choice == 'n':
        INSERT_EVENT.clear()
        
        return False



if __name__ == "__main__":
    insert = Thread(target=insert_data)
    insert.setDaemon(True)
    insert.start()

    while True:
        res = main()
        if res:
            print("已经开始插入数据了")
        else:
            print("停止插入数据了")



