from models.dbmanip import DBManip
from models.model import Model
from models.list import List

class Manager:
	def __init__(self):
		self.model = None
		self.currUserId = 1


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
		""" Performing necessary actions to load lists view 
			TODO
		"""	
		lists = self.model.GetUserLists(self.currUserId)
		return lists

	def GoToListWizard(self):
		""" Performing necessary actions to load lists view 
			TODO
		"""	
		print("TO DO: Add new list wizard")

	def SubmitListAndGoToConfirm(self, name):
		""" Sends data to database, wait for confirmation (id of created list) 
			name - name of a new list
		returns: None
		"""	
		print("Adding new list to database...")
		result = self.model.CreateList(name, self.currUserId)
		if len(result) > 0:
			print("Adding complete!")
		else:
			print("I cannot add your new list.")
		

if __name__ == "__main__":
#app start
    manager = Manager()
    manager.SetupSystem() 