import random
from dbmanip import DBManip
from list import List

class Model:
	def __init__(self, initialized_db):
		self.listCols = ["identifier", "name", "user_id", "created_at", "updated_at"]
		self.listTable = "lists"
		self.listPrefix = "pom1_"
		self.db = initialized_db

	def CreateList(self, name, user_id):
		""" Creates new list in database
			name - name of the list
			user_id - id of the owner
		returns: new List
		"""
		print("Creating new list in database")
		lst = List()
		lst.identifier = self.ObtainListId()
		lst.name = name
		lst.user_id = user_id

		self.db.Insert(\
			{self.listCols[0]:lst.identifier , \
			self.listCols[1]:lst.name, \
			self.listCols[2]:lst.user_id, \
			self.listCols[3]:lst.created_at, \
			self.listCols[4]:lst.updated_at}, \
			self.listTable)

		return lst

	def ObtainListId(self):
		""" Generates new, unique id for list and check its uniqueness
		returns: new, unique id
		"""
		newId = ""
		while True:
			randstr = ("%08x" % random.getrandbits(32))
			newId = self.listPrefix + randstr
			print("Generated new task id: {}".format(newId))
			
			whereStatement = self.listCols[0] + "='" + newId + "'"
			res = self.db.Select(self.listCols[:1], self.listTable, whereStatement)
			if len(res) == 0:
				break;
		return newId

	def ChangeList(self, list_id, name):
		""" Perform changes in given list in database
			list_id - id of the list
			name - name of the list
			user_id - id of the owner
		returns: new List
		"""
		print("Modyfing list data in database")

		self.db.Update(\
			{self.listCols[1]:lst.name, \
			self.listCols[4]:lst.updated_at}, \
			self.listTable)

		lst = GetSingleList(list_id)
		lst.name = name
		
		return lst

	def GetSingleList(self, list_id):
		""" Gets exact list (based on given list_id)
		returns: single list
		"""
		print("Fetching single list from database")
		whereStatement = "{} = {}".format(self.listCols[0], list_id)
		rawResult = self.db.Select(self.listCols, self.listTable, whereStatement)
		singleList = self.ListRawToObj(rawResult)
		return singleList

	def GetUserLists(self, user_id):
		""" Gets every list that belongs to the user_id
			user_id - id of user
		returns: list of List objects
		"""
		print("Fetching lists from database")
		whereStatement = "user_id = {}".format(user_id)
		rawResult = self.db.Select(self.listCols, self.listTable, whereStatement)
		
		lists = []
		for rawList in rawResult:
			lists.append(self.ListRawToObj(rawList))
		
		return lists

	def ListRawToObj(self, raw):
		""" Initialize list with raw values
			raw - dictionary; keys - col names, values - resp vals
		returns: List obj
		"""
		lst = List()
		lst.identifier = raw[self.listCols[0]]
		lst.name = raw[self.listCols[1]]
		lst.user_id = raw[self.listCols[2]]
		lst.created_at = raw[self.listCols[3]]
		lst.updated_at = raw[self.listCols[4]]
		return lst
