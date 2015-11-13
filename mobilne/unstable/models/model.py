import random
from dbmanip import DBManip
from list import List

class Model:
	def __init__(self, initialized_db):
		self.listCols = ["identifier", "name", "user_id", "created_at", "updated_at"]
		self.listTable = "lists"
		self.db = initialized_db

	def CreateList(self, name, user_id):
		""" Creates new list in database
			name - name of a list
			user_id - id of the owner
		returns: new List
		"""
		print("Creating new list in database")
		lst = List()
		lst.identifier = #obtain new id
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
		""" Generates new, unique id for list. Check its unique by compare with existing ids
		returns: new, unique id
		"""
		randstr = ("%08x" % random.getrandbits(32))
		# dshffffffffffffgfdgdfdghdhgfdghfdhgdhgfdhgfdghfdhgfdghfdghfdghfdghfdhgfdhgfdhgfdhgfdhgfdhgdhf



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
