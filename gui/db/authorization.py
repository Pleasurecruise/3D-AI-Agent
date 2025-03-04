import os
import sqlite3
import threading
import functools

# 确保只有一个线程可以访问数据库
def synchronized(func):
  @functools.wraps(func)
  def wrapper(self, *args, **kwargs):
    with self.lock:
      return func(self, *args, **kwargs)
  return wrapper

class Authorization:
    def __init__(self):
        self.cursor = None
        self.conn = None
        self.lock = threading.Lock()

    def init_db(self):
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), '../../assets/db/authorization.db'))
        self.cursor = self.conn.cursor()
        self.cursor.execute(
        '''
            CREATE TABLE IF NOT EXISTS authorize
            (id INTEGER PRIMARY KEY     autoincrement,
            userid        char(100),
            accesstoken           TEXT,
            expirestime           BigInt,
            createtime         Int);
        ''')
        self.conn.commit()
        self.conn.close()

    @synchronized
    def insert(self, userid, accesstoken, expirestime, createtime):
        self.init_db()
        self.conn = sqlite3.connect("authorization.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            '''
            INSERT INTO authorize (userid, accesstoken, expirestime, createtime)
            VALUES (?, ?, ?, ?)
            ''', (userid, accesstoken, expirestime, createtime)
        )
        self.conn.commit()
        self.conn.close()
        return self.cursor.lastrowid

    @synchronized
    def search_by_userid(self, userid):
        self.init_db()
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), '../../assets/db/authorization.db'))
        self.cursor = self.conn.cursor()
        self.cursor.execute(
        '''
        SELECT * FROM Authorize WHERE userid=?
            ''', (userid,))
        result = self.cursor.fetchone()
        self.conn.close()
        return result

    @synchronized
    def update(self, userid, new_accesstoken, new_expirestime):
        self.init_db()
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), '../../assets/db/authorization.db'))
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            '''
            UPDATE Authorize SET accesstoken=?, expirestime=? WHERE userid=?
            ''', (new_accesstoken, new_expirestime, userid))
        self.conn.commit()
        self.conn.close()