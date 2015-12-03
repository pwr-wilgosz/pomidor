from models.dbmgr import DBMgr
# from models.model import Model
from models.listmodel import ListModel
from gui.main import PomidorApp
from servcomm import ServComm

defaultServer = 'http://tomato-cal.herokuapp.com'
defaultLogin = 'rekonfiguracja@projekt.pwr'
defaultPass = 'listy_zadan'

class Manager:
	def __init__(self):
		self.db = None
		self.gui = None
		self.servComm = None
		self.currUserId = None
		self.servAuth = None
		self.pickedListId = None
		self.pickedTaskId = None


	def SetupSystem(self):
		""" Initializing system components
		"""
		self.db = DBMgr()
		self.gui = PomidorApp(self)
		self.servComm = ServComm(defaultServer)

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


	def PickedListTaskData(self):
		""" Returns picked by user list and task raw data pairs
		returns: two items: listName and taskRaw
		"""
		listName = None
		taskRaw = None
		if self.pickedListId != None:
			pickedList = self.db.GetSingleList(self.pickedListId)
			listName = pickedList.name
		if self.pickedTaskId != None:
			pickedTask = self.db.GetSingleTask(self.pickedTaskId)
			taskRaw = [pickedTask.IdNamePriorDict()]

		return listName, taskRaw

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

	def SubmitTask(self, name, prior, duration):
		""" Sends data to database, wait for confirmation
			name - name of a new task
			prior - priority
			duration - time that task is predicted to finish (in pomodoro cycles)
		returns:  bool - confirmation. True - ok
		"""
		return self.db.AddTask(name, self.pickedListId, prior, duration)

	def ModifyTask(self, task_id, name = None, dur = None, prior = None):
		""" Changes task data in database, wait for confirmation
			task_id - identifier of given task
			name - name of a new task
		returns:  bool - confirmatin. True - ok
		"""
		print("Changing task in database...")
		return self.db.ModifyTask(task_id, name, dur, prior)

	def DeleteTask(self, task_id):
		""" Removes data from database, wait for confirmation
			task_id - task identifier
		returns: bool - confirmatin. True - ok
		"""
		return self.db.DelTask(task_id)

if __name__ == "__main__":
#app start
	manager = Manager()
	manager.SetupSystem()
	manager.RunGui()
