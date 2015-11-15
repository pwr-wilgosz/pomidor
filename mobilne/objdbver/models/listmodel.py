from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
import random
from base import Base

class ListModel(Base):
	__tablename__ = 'lists'
	listPrefix = 'rpi_'

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

	def Modify(self, name):
		""" Modyfies record args and set updated_at datetime
			name - changed name
		returns self
		"""
		self.name = name
		self.updated_at = datetime.now()
		return self