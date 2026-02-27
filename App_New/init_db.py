import sqlite3

conn = sqlite3.connect('donors.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS donors')
cursor.execute('''
    CREATE TABLE donors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        blood_group TEXT NOT NULL,
        state TEXT NOT NULL,
        district TEXT NOT NULL,
        locality TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
print("New Advanced Database Rebuilt Successfully! 🚀")