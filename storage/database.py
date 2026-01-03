import sqlite3

class Database:
    def __init__(self, path="ds_method.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)

    def insert(self, table, data: dict):
        keys = ",".join(data.keys())
        q = ",".join(["?"] * len(data))
        sql = f"INSERT OR REPLACE INTO {table} ({keys}) VALUES ({q})"
        self.conn.execute(sql, tuple(data.values()))
        self.conn.commit()
