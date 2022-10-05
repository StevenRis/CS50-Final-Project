import sqlite3

con = sqlite3.connect("database.db")

con.execute('''CREATE TABLE locations (id INTEGER PRIMARY KEY,
location TEXT,
FOREIGN KEY (id) REFERENCES cars(id))''')
# con.execute('INSERT INTO cars (car_brand, car_model) VALUES ("Ford", "Focus")')
con.commit()

