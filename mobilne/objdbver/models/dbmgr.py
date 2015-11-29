from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import os.path
#ORM types
from datetime import datetime
import base
from listmodel import ListModel

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
