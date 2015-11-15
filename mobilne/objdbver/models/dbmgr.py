from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import os.path
#ORM types
from datetime import datetime


Base = declarative_base()
class ListModel(Base):
	__tablename__ = 'lists'
	listPrefix = 'pom1_'

	identifier = Column(String, primary_key=True)
	name = Column(String, nullable=False)
	user_id = Column(Integer)
	created_at = Column(DateTime, default=datetime.now(), nullable=False)
	updated_at = Column(DateTime, default=datetime.now(), nullable=False)

	def __init__(self, in_name, in_uid, \
		in_id=None, in_crat=datetime.now(), in_upat=datetime.now()):
		if in_id == None:
			in_id = self.ObtainListId()		
		self.identifier = in_id
		self.name = in_name
		self.user_id = in_uid
		self.created_at = in_crat
		self.updated_at = in_upat

	def __str__(self):
		return "Lista '{nazwa}', utworzona {cr}, modyfikowana {mod}"\
			.format(nazwa=self.name, \
				cr=self.created_at.strftime("%d %b %Y, %H:%M"), \
				mod=self.updated_at.strftime("%d %b %Y, %H:%M"))
	def __repr__(self):
		return self.__str__()

	def ObtainListId(self):
		""" Generates id for list
		returns: new id
		"""
		randstr = ("%08x" % random.getrandbits(32))
		newId = self.listPrefix + randstr
		print("Generated new task id: {}".format(newId))
		return newId

class DBMgr():
	# Database connection
	DB_FILE = 'db.sqlite3'
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
		  Base.metadata.create_all(self.engine)
		# Create a bunch of records if we don't have any
		if self.session.query(ListModel).count() == 0:
		   print("Creating new list in database")
			lst = ListModel(name, user_id)
			self.session.add(lst)