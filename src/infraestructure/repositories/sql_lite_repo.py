import sqlite3
import os
from threading import Lock


class SQLiteConnect:
    def __init__(self, db_path="trading.db"):
        self.db_path = db_path

    # --------------------------------------
    # Obtener conexion
    # --------------------------------------
    def get_conn(self):
        os.makedirs(self.db_path, exist_ok=True)
        return sqlite3.connect(self.db_path, check_same_thread=False)

    # ---------------------------------------
    # Crear tablas
    # ---------------------------------------
    def create_tables(self):
        conn = self.get_conn()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS executions (
                exec_id TEXT PRIMARY KEY,
                con_id INTEGER,
                symbol TEXT,
                sec_type TEXT,
                right TEXT,
                strike REAL,
                side TEXT,
                qty REAL,
                price REAL,
                exec_time TEXT,
                account TEXT,
                exchange TEXT,
                trade_id INTEGER
            )
        """)
            conn.commit()
        finally:
            conn.close()


# Repositorios


class ExecutionsRepositorySQL:
    def __init__(self, db):
        self.db = db
        self.lock = Lock()

    def save(self, exec_data):
        with self.lock:
            conn = self.db.get_conn()
            try:
                cursor = conn.cursor()
                params = (
                    exec_data["exec_id"],
                    exec_data["con_id"],
                    exec_data["symbol"],
                    exec_data["sec_type"],
                    exec_data["right"],
                    exec_data["strike"],
                    exec_data["side"],
                    exec_data["qty"],
                    exec_data["price"],
                    exec_data["exec_time"],
                    exec_data["account"],
                    exec_data["exchange"],
                )

                query = """
                    INSERT OR IGNORE INTO executions (
                        exec_id, con_id, symbol, sect_type, right, strike, side, qty, price, exec_time, account, exchange
                        ) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """

                cursor.execute(query, params)
                conn.commit()
            except Exception as e:
                raise Exception(f"Error saving execution: {str(e)}")
