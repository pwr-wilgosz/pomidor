from datetime import datetime

class List:
	def __init__(self):
		self.identifier = ""
		self.name = ""
		self.user_id = 0
		self.created_at = datetime.now()
		self.updated_at = datetime.now()

	def __str__(self):
		return "Lista '{nazwa}', utworzona {cr}, modyfikowana {mod}"\
			.format(nazwa=self.name, \
				cr=self.created_at.strftime("%d %b %Y, %H:%M"), \
				mod=self.updated_at.strftime("%d %b %Y, %H:%M"))