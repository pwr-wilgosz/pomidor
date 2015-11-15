from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from kivy.graphics import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.app import App
import os.path


# Database connection
DATABASE = 'sqlite:///db.sqlite3'
DEBUG = True

# ORM base
Base = declarative_base()


# Connect to database
engine = create_engine(DATABASE, echo=DEBUG)
session_factory = sessionmaker(bind=engine)
session = session_factory()

# Initialize database if it doesn't exist
if not os.path.exists('db.sqlite3'):
  Base.metadata.create_all(engine)

# ORM types
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


# Create a bunch of records if we don't have any
if session.query(MyRecord).count() == 0:
  for i in range(10):
    record = MyRecord('key%d' % i, 'value%d' % i)
    session.add(record)

# Kivy widget for a 'MyRecord' type; notice how it extends BoxLayout
class MyRecordWidget(BoxLayout):
  def __init__(self, record, **kwargs):
    super(MyRecordWidget, self).__init__(**kwargs)
    self.add_widget(Label(text=record.key))
    self.add_widget(Label(text=record.value))

# App loads all records and puts them into a ui
class MyApp(App):
  def build(self):
    layout = BoxLayout(orientation='vertical')
    records = session.query(MyRecord).all()
    for r in records:
      widget = MyRecordWidget(r)
      layout.add_widget(widget)
    return layout

if __name__ == '__main__':
  MyApp().run()