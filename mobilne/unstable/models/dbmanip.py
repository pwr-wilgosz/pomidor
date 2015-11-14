import sqlite3

class DBManip:
	def __init__(self):
		file = '/home/rafszt/Programowanie/pomidor/mobilne/unstable/models/pomidor_db.sqlite'
		self.conn = sqlite3.connect(file, detect_types=sqlite3.PARSE_DECLTYPES)
		

	def Write(self, sqlCommand):
		c = self.conn.cursor()
		c.execute(sqlCommand)
		self.conn.commit()
		
	def Read(self, sqlCommand):
		c = self.conn.cursor()
		c.execute(sqlCommand)
		return c.fetchall()

	def Select(self, cols, from_tab, where = 1):
		""" Perform SQL select query, given 
			cols - table of strings
			from - name of table
			where - conditions """
		cols_str = ", ".join(cols)
		select_str = "SELECT {w} FROM {f} WHERE {wh}".\
					format(w=cols_str, f=from_tab, wh=where)
		print(select_str)
		read = self.Read(select_str)
		packedResult = self.PackResult(cols, read)
		return packedResult
		
	def PackResult(self, cols, result):
		""" Convert raw output into list of dictionaries """
		packedResult = []
		for rowInd in range(len(result)):
			tempDict = dict()
			for colInd in range(len(cols)):
				tempDict[cols[colInd]] = result[rowInd][colInd]

			packedResult.append(tempDict)
		return packedResult	

	def Insert(self, data, dest_tab):
		""" Perform SQL insert query, given 
			data - col-value dictionary  
			dest_tab - name of table """
		cols_str = ", ".join(data.keys())
		data_str = "(\"" + "\", \"".join(map(str, data.values())) + "\")"
		insert_str = "INSERT INTO {dt} ({col}) VALUES {vals}".\
					format(dt=dest_tab, col=cols_str, vals=data_str)
		self.Write(insert_str)	

	def Update(self, tab, data, where):
		""" Perform SQL update query, given 
			tab - name of table
			data - col-new_value dictionary  
			where - conditions that select rows to modify
		returns: None 
		"""
		set_tab = []
		for it in range(len(myDict)):
			set_tab.append("{}='{}'".format(myDict.keys()[it], myDict.values()[it]))
		set_str = ", ".join(set_tab)	
		insert_str = "UPDATE {t} SET {s} WHERE {w}".\
					format(t=tab, s=set_str, w=where)
		self.Write(insert_str)	

	def __exit__(self, exc_type, exc_value, traceback):
		self.conn.commit()
		self.conn.close()

