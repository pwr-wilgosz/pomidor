from models.dbmanip import DBManip
from models.list import List

class Model:
	def __init__(self, initialized_db):
		self.db = initialized_db

	def CreateList(self, name, user_id):
		""" Creates new list in database
			name - name of a list
			user_id - id of the owner
		returns: id of a new list
		"""
		print("TO DO: Creating new list in database")

	def GetAllLists(self, user_id):
		""" Gets every list that belongs to the user_id
			user_id - id of user
		returns: list of List objects
		"""
		print("TO DO: Fetching lists from database")

