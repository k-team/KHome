import sqlite3

conn = sqlite3.connect('scutu.db')

c = conn.cursor()
c.execute('SELECT ...')
conn.commit()
conn.close()
