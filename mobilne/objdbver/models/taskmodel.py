from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import random
# from listmodel import ListModel
from base import Base

class TaskModel(Base):
	__tablename__ = 'tasks'
	taskPrefix = 'rpi_'

	identifier = Column(String, primary_key=True)
	name = Column(String, nullable=False)
	list_id = Column(ForeignKey(u'lists.identifier', ondelete=u'CASCADE'), nullable=False)
	created_at = Column(DateTime, default=datetime.now(), nullable=False)
	updated_at = Column(DateTime, default=datetime.now(), nullable=False)
	duration = Column(Integer, default=1, nullable=False)
	priority = Column(Integer, default=1, nullable=False)

	mylist = relationship(u'ListModel')

	def __init__(self, in_name, in_list_id, in_prior = 1, in_dur = 1,\
		in_id=None, in_crat=datetime.now(), in_upat=datetime.now()):

		if in_id == None:
			in_id = self.ObtainTaskId()
		self.identifier = in_id
		self.name = in_name
		self.list_id = in_list_id
		self.created_at = in_crat
		self.updated_at = in_upat
		self.duration = in_dur
		self.priority = in_prior

	def __str__(self):
		return "Zadanie '{nazwa}' listy o id '{list_id}', utworzone {cr}, modyfikowane {mod}"\
			.format(nazwa=self.name, list_id=self.list_id,\
				cr=self.created_at.strftime("%d %b %Y, %H:%M"), \
				mod=self.updated_at.strftime("%d %b %Y, %H:%M"))

	def __repr__(self):
		return self.__str__()

	def ObtainTaskId(self):
		""" Generates id for list
		returns: new id
		"""
		randstr = ("%08x" % random.getrandbits(32))
		newId = self.taskPrefix + randstr
		print("Generated new task id: {}".format(newId))
		return newId

	def Modify(self, name = None, prior = None, duration = None):
		""" Modyfies record args and set updated_at datetime
			name - changed name (optional)
			prior - changed priority (optional)
			duration - changed duration (optional)
		returns self
		"""
		if name != None:
			self.name = name
		if prior != None:
			self.priority = prior
		if duration != None:
			self.duration = duration
		self.updated_at = datetime.now()
		return self

	def IdNamePriorDict(self):
		""" Function that returns model as dict of values for display purpose
		returns: dict of id, name, prior properties
		"""
		d = dict()
		d['id'] = self.identifier
		d['name'] = self.name
		d['prior'] = self.priority
		return d
