from sqlalchemy import Column, Integer, String
from base import Base

class MyRecord(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)

    def __init__(self, key, value):
      self.key = key
      self.value = value

    def __repr__(self):
        return "<Record('%s = %s')>" % (self.key, self.value)