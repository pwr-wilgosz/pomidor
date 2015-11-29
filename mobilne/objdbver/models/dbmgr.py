from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.exc import SQLAlchemyError
import os.path
#ORM types
from datetime import datetime
import base
from listmodel import ListModel
from taskmodel import TaskModel

class DBMgr():
	# Database connection
	DB_FILE = 'pom_db.sqlite'
	DB_LINK = 'sqlite:///' + DB_FILE
	DEBUG = True

	def __init__(self):
		# ORM base
		self.Connect()
		self.InitDB()

	def Connect(self):
		""" Connect to database
		"""
		self.engine = create_engine(\
			self.DB_LINK, echo=self.DEBUG)
		session_factory = sessionmaker(bind=self.engine)
		self.session = session_factory()


	def InitDB(self):
		""" Init database if it doesn't exists
		"""
		if not os.path.exists(self.DB_FILE):
			base.Base.metadata.create_all(self.engine)

		# # Create a bunch of records if we don't have any
		# self.session.query(ListModel).count()
		# 	print("Creating new list in database")
		# lst = ListModel("name", 1)
		# self.session.add(lst)
		# self.session.commit()

	def Comm(self):
		""" Performs commit to database with simple exception handling
		returns : True if there wasn't any problem, False otherwise
		"""
		try:
			self.session.commit()
		except SQLAlchemyError:
			return False
		return True

	#LISTS PART
	def ModifyList(self, list_id, name):
		""" Perform changes in given list in database
			list_id - id of the list
			name - name of the list
			user_id - id of the owner
		returns: bool confirmation (True - ok, False - fail)
		"""
		print("Modyfing list data in database")
		lst = self.GetSingleList(list_id)
		lst.Modify(name)
		return self.Comm()

	def GetSingleList(self, list_id):
		""" Gets exact list (based on given list_id)
		returns: single list
		"""
		print("Fetching single list from database")
		singleList = self.session.query(ListModel).\
			filter_by(identifier=list_id).first()
		return singleList

	def DelList(self, list_id):
		""" Dellete exact list (based on given list_id)
		returns: bool confirm; True - ok
		"""
		listToDel = self.GetSingleList(list_id)
		self.session.delete(listToDel)
		return self.Comm()

	def GetUserLists(self, user_id):
		""" Gets every list that belongs to the user_id
			user_id - id of user
		returns: list of List objects
		"""
		print("Fetching lists from database")
		lists = self.session.query(ListModel).\
			filter_by(user_id="{uid}".format(uid=user_id)).all()
		return lists

	def AddList(self, name, user_id):
		""" Adds list to database
			name - name of a new list
		returns: None
		"""
		print("Creating list")
		newList = ListModel(name, user_id)
		print("Sending list to database")
		self.session.add(newList)
		return self.Comm()

	#TASKS PART
	def ModifyTask(self, task_id, name = None, dur = None, prior = None):
		""" Perform changes in given task in database
			task_id - id of the task
			name - name of the task (optional)
			dur - duration of the task (optional)
			prior - priority of the task (optional)
		returns: bool confirmation (True - ok, False - fail)
		"""
		print("Modyfing task data in database")
		lst = self.GetSingleTask(task_id)
		lst.Modify(name, prior, dur)
		return self.Comm()

	def GetSingleTask(self, task_id):
		""" Gets exact task (based on given task_id)
		returns: single task
		"""
		print("Fetching single task from database")
		singleTask = self.session.query(TaskModel).\
			filter_by(identifier=task_id).first()
		return singleTask

	def DelTask(self, task_id):
		""" Dellete exact task (based on given task_id)
		returns: bool confirm; True - ok
		"""
		taskToDel = self.GetSingleTask(task_id)
		self.session.delete(taskToDel)
		return self.Comm()

	def GetListTasks(self, in_list_id):
		""" Gets every task that are assigned to given list
			in_list_id - id of given list
		returns: list of Task objects
		"""
		print("Fetching tasks from database")
		tasks = self.session.query(TaskModel).\
			filter_by(list_id="{lid}".format(lid=in_list_id)).all()
		return tasks

	def AddTask(self, name, list_id, prior):
		""" Adds task to database
			name - name of a new task
			list_id - list that new task will belong to
			prior - priority of new task
		returns: None
		"""
		print("Creating task")
		newTask = TaskModel(name, list_id, prior)
		print("Sending task to database")
		self.session.add(newTask)
		return self.Comm()
