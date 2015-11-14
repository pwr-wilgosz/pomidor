from dbmanip import DBManip

db = DBManip()

# tabela listy
# db.Write('CREATE TABLE lists (\
# 	identifier TEXT PRIMARY KEY,\
# 	name TEXT,\
# 	user_id INTEGER,\
# 	created_at TIMESTAMP NOT NULL,\
# 	updated_at TIMESTAMP NOT NULL)')

# tabela zadania
# db.Write('CREATE TABLE tasks (\
# 	identifier TEXT PRIMARY KEY,\
# 	name TEXT,\
# 	list_identifier TEXT,\
# 	duration INTEGER,\
# 	priority INTEGER,\
# 	created_at TIMESTAMP NOT NULL,\
# 	updated_at TIMESTAMP NOT NULL,\
# 	FOREIGN KEY (list_identifier) REFERENCES lists(identifier))')

#trigger aktualizujacy date modyfikacji listy
# db.Write('CREATE TRIGGER update_list_mod_date \
# 		AFTER UPDATE ON lists FOR EACH ROW \
# 		WHEN NEW.updated_at <> OLD.updated_at  \
#   	BEGIN\
#     	 UPDATE lists SET updated_at=CURRENT_TIMESTAMP WHERE identifier=OLD.identifier;\
#   	END;')

# trigger testowy
db.Write("create trigger update_list AFTER UPDATE ON lists FOR EACH ROW WHEN NEW.updated_at<OLD.updated_at\
	begin\
		UPDATE lists SET updated_at=CURRENT_TIMESTAMP WHERE identifier=OLD.identifier;\
	end;")
