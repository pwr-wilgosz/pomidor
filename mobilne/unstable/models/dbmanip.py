import sqlite3

class DBManip:
	def __init__(self):
		file = './pomidor_db.sqlite'
		self.conn = sqlite3.connect(file)
		

	def Write(self, sqlCommand):
		c = self.conn.cursor()
		c.execute(sqlCommand)
		self.conn.commit()
		
	def Read(selg, sqlCommand):
		c = self.conn.cursor()
		c.execute(sqlCommand)
		return c.fetchall()

	def __exit__(self, exc_type, exc_value, traceback):
		self.conn.close()

