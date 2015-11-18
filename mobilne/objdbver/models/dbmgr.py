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

	def ChangeList(self, list_id, name):
		""" Perform changes in given list in database
			list_id - id of the list
			name - name of the list
			user_id - id of the owner
		returns: new List
		"""
		print("Modyfing list data in database")
		lst = GetSingleList(list_id)
		lst.Modify(name)
		self.session.commit()
		return lst

	def GetSingleList(self, list_id):
		""" Gets exact list (based on given list_id)
		returns: single list
		"""
		print("Fetching single list from database")
		singleList = self.session.query(ListModel).\
			filter_by(identifier=list_id).first()
		return singleList

	def GetUserLists(self, user_id):
		""" Gets every list that belongs to the user_id
			user_id - id of user
		returns: list of List objects
		"""
		print("Fetching lists from database")
		lists = self.session.query(ListModel).\
			filter_by(user_id="{uid}".format(uid=user_id)).all()
		return lists