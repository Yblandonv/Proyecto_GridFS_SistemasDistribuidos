import sqlite3

def crear_tabla_datanodes():
    conn = sqlite3.connect('bloques.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS datanodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()