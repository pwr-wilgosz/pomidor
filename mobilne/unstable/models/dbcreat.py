from dbmanip import DBManip

db = DBManip()

#tabela listy
db.Write('CREATE TABLE lists (\
	identifier TEXT PRIMARY KEY,\
	name TEXT,\
	user_id INTEGER,\
	created_at TIMESTAMP NOT NULL,\
	updated_at TIMESTAMP NOT NULL)')

#tabela zadania
db.Write('CREATE TABLE tasks (\
	identifier TEXT PRIMARY KEY,\
	name TEXT,\
	list_identifier TEXT,\
	duration INTEGER,\
	priority INTEGER,\
	created_at TIMESTAMP NOT NULL,\
	updated_at TIMESTAMP NOT NULL,\
	FOREIGN KEY (list_identifier) REFERENCES lists(identifier))')