from models.dbmgr import DBMgr
from models.model import Model
from models.list import List
from gui.main import PomidorApp

class Manager:
	def __init__(self):
		self.db = None
		self.gui = None
		self.currUserId = 1


	def SetupSystem(self):
		""" Initializing system components
		"""
		self.db = DBMgr()
		self.gui = PomidorApp()

	def RunGui(self):
		""" Run graphical mode
		"""
		self.gui.run()

	def Sync(self):
		""" Performing synchronize procedures with serwer
			TODO
		"""
		print("TO DO: Performing sync with server")

	def GoToListsView(self):
		""" Performing necessary actions to load lists view
			TODO
		"""
		lists = self.db.GetUserLists(self.currUserId)
		return lists

	def GoToListWizard(self):
		""" Actions requied to open add-new-list wizard
			TODO
		"""
		print("TO DO: Add new list wizard")

	def SubmitList(self, name):
		""" Sends data to database, wait for confirmation (new list obj)
			name - name of a new list
			TODO
		returns: None
		"""
		print("Adding new list to database...")
		result = self.model.CreateList(name, self.currUserId)
		if len(result) > 0:
			print("Adding complete!")
		else:
			print("I cannot add your new list.")

	def GoToModifyWizad(self):
		""" Loads single list in purpose of edit
			TODO
		returns: None
		"""
		print("TO DO: Loading modify-list window...")

	def SubmitListChangesAndGoToConfirm(self, list_id, name):
		""" Sends data to database, wait for confirmation (modified list obj)
			name - name of a new list
			TODO
		returns: None
		"""
		print("Changing list in database...")
		result = self.model.ChangeList(list_id, name)
		if len(result) > 0:
			print("Saving complete!")
		else:
			print("I cannot perform changes.")



if __name__ == "__main__":
#app start
    manager = Manager()
    manager.SetupSystem()
	manager.RunGui()
