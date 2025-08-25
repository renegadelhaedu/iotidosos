import sqlite3



class DatabaseHandler:
    def __init__(self, db_name='sensor_monitoring.db'):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS sensor_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            casa_id TEXT NOT NULL,
            tipo_alerta TEXT NOT NULL,
            data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        '''
        with self.get_connection() as conn:
            conn.execute(create_table_query)
            conn.commit()

    def insert_log(self, casa_id, tipo_alerta):
        insert_query = '''
        INSERT INTO sensor_logs (casa_id, tipo_alerta)
        VALUES (?, ?)
        '''
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(insert_query, (casa_id, tipo_alerta))
            conn.commit()
            return cursor.lastrowid

    def get_all_logs(self):
        select_query = '''
        SELECT id, casa_id, tipo_alerta, data_hora
        FROM sensor_logs
        ORDER BY data_hora DESC
        '''
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(select_query)
            return cursor.fetchall()

    def get_logs_by_casa(self, casa_id):
        select_query = '''
        SELECT id, casa_id, tipo_alerta, data_hora
        FROM sensor_logs
        WHERE casa_id = ?
        ORDER BY data_hora DESC
        '''
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(select_query, (casa_id,))
            return cursor.fetchall()

    def get_logs_by_tipo(self, tipo_alerta):
        select_query = '''
        SELECT id, casa_id, tipo_alerta, data_hora
        FROM sensor_logs
        WHERE tipo_alerta = ?
        ORDER BY data_hora DESC
        '''
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(select_query, (tipo_alerta,))
            return cursor.fetchall()