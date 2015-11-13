from models.dbmanip import DBManip
from models.model import Model
from models.list import List

class Manager:
	def __init__(self):
		self.model = None


	def SetupSystem(self):
		""" Initializing system components
		"""
		db = DBManip()
		self.model = Model(db)

	def Sync(self):
		""" Performing synchronize procedures with serwer
			TODO
		"""
		print("TO DO: Performing sync with server")

	def GoToListsView(self):
		""" Performing necessary actions to load proper view 
			TODO
		"""	
		

if __name__ == "__main__":
#app start
    manager = Manager()
    manager.SetupSystem() 