from models.dbmgr import DBMgr
# from models.model import Model
from models.listmodel import ListModel
from gui.main import PomidorApp

class Manager:
	def __init__(self):
		self.db = None
		self.gui = None
		self.currUserId = None
		self.servAuth = None
		self.pickedListId = None
		self.pickedTaskId = None


	def SetupSystem(self):
		""" Initializing system components
		"""
		self.db = DBMgr()
		self.gui = PomidorApp(self)

		self.RunDB()
		#self.RunGui()

	def RunDB(self):
		""" Establish DB (internal) connection
		"""
		self.db.Connect()

	def RunGui(self):
		""" Run graphical mode
		"""
		self.gui.run()

	def LoginToApp(self, auth_name = None, auth_pass = None):
		""" Specify data required to pass server ath during sync
			and id of an current user.
			FUTURE - user will be add to the local base, data for auth
			will be	invoke from the local db
			auth_name - user login
			auth-pass - user pass
			id - unique id of an user
		returns: string
			'OK' if user record egsists in local db
			'ServReq' if doesn't egists. server auth is required
			'Fail' if user of such login egists but pass is incorrect
		"""
		# hard set
		self.currUserId = 1
		return 'OK'


	def ConnectAndSync(self, auth_name, auth_pass):
		""" Establish connection with server and perform sync
		returns: string
			'OK' if sync goes right
			'Error' if serv response is not recognised
			'UserFail' if there was incorrect login data
		"""
		res = None
		if self.servAuth == None:
			# after implementation of user table, if there will be
			# confirmed user, get auth data from user objects;
			res = self.LoginToRemote(auth_name, auth_pass)
		if res != 'OK':
			return res

		res = self.Sync()
		return res

	def LoginToRemote(self, auth_name, auth_pass):
		""" Connects to server, veryfies login data, gets auth-key for sync
		returns: string
			'OK' if user login correctly
			'Error' if serv response is not recognised
			'UserFail' if user of such login exists but pass is incorrect
		"""
		# Set auth-key
		return 'OK'

	def Sync(self):
		""" Performing synchronize procedures with server
		returns: string
			'OK' if user login correctly
			'Error' if serv response is not recognised
		"""
		return 'OK'


	#LISTS
	def GetListsToView(self):
		""" Performing necessary actions to load lists view
			FIRES: after gui call
		returns: dictionary of id-name pairs from record
		"""
		listsToDisp = dict()
		listsFromDB = self.db.GetUserLists(self.currUserId)
		listRepr = None
		for r in listsFromDB:
			listRepr = r.IdNamePair()
			listsToDisp[listRepr[0]] = listRepr[1]
		return listsToDisp


	def SubmitList(self, name):
		""" Sends data to database, wait for confirmation (new list obj)
			name - name of a new list
		returns:  bool - confirmatin. True - ok
		"""
		return self.db.AddList(name, self.currUserId)
		# Old way
		# print("Adding new list to database...")
		# result = self.model.CreateList(name, self.currUserId)
		# if len(result) > 0:
		# 	print("Adding complete!")
		# else:
		# 	print("I cannot add your new list.")

	def ModifyList(self, list_id, new_name):
		""" Changes lists data in database, wait for confirmation (new list obj)
			list_id - identifier of given list
			new_name - name of a new list
		returns:  bool - confirmatin. True - ok
		"""
		print("Changing list in database...")
		return self.db.ModifyList(list_id, new_name)

	def DeleteList(self, list_id):
		""" Removes data from database, wait for confirmation (new list obj)
			list_id - list identifier
		returns: bool - confirmatin. True - ok
		"""
		return self.db.DelList(list_id)

	def SetList(self, list_id):
		""" Store user list pick (list_id)
			list_id - id of picked list
		returns: None
		"""
		self.pickedListId = list_id
		self.pickedTaskId = None

	def SetTask(self, task_id):
		""" Store user task pick from given list (tasj_id)
			task_id - id of picked task
		returns: None
		"""
		self.pickedTaskId = task_id

	def PickedListTaskNamePair(self):
		""" Returns picked by user list and task ids pairs
		returns: two items: list_id and task_id
		"""
		listName = None
		if self.pickedListId != None:
			pickedList = self.db.GetSingleList(self.pickedListId)
			listName = pickedList.name

		return listName, self.pickedTaskId

	#TASKS
	def GetTasksToView(self):
		""" Performing necessary actions to load tasks view
			FIRES: after gui call
		returns: list of id - name - prior dictionaries
		"""
		tasksToDisp = []
		if self.pickedListId == None:
			return tasksToDisp

		tasksFromDB = self.db.GetListTasks(self.pickedListId)
		for r in tasksFromDB:
			tasksToDisp.append(r.IdNamePriorDict())
		return tasksToDisp


	def SubmitTask(self, name):
		""" Sends data to database, wait for confirmation (new list obj)
			name - name of a new list
		returns:  bool - confirmatin. True - ok
		"""
		return self.db.AddTask(name, self.currUserId)
		# Old way
		# print("Adding new list to database...")
		# result = self.model.CreateTask(name, self.currUserId)
		# if len(result) > 0:
		# 	print("Adding complete!")
		# else:
		# 	print("I cannot add your new list.")

	def ModifyTask(self, list_id, new_name):
		""" Changes lists data in database, wait for confirmation (new list obj)
			list_id - identifier of given list
			new_name - name of a new list
		returns:  bool - confirmatin. True - ok
		"""
		print("Changing list in database...")
		return self.db.ModifyTask(list_id, new_name)

	def DeleteTask(self, list_id):
		""" Removes data from database, wait for confirmation (new list obj)
			list_id - list identifier
		returns: bool - confirmatin. True - ok
		"""
		return self.db.DelTask(list_id)



if __name__ == "__main__":
#app start
	manager = Manager()
	manager.SetupSystem()
	manager.RunGui()
