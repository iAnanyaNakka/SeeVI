import sqlite3

def setup_db():
	db = sqlite3.connect("users.db")
	cursor = db.cursor()
	
	cursor.execute("""CREATE TABLE IF NOT EXISTS users (
     									username  TEXT NOT NULL,
										passwd text NOT NULL,
										fname text NOT NULL,
										age integer NOT NULL,
										rarestage text NOT NULL,
          								colorpreferred text NOT NULL,
										posturepreferred text NOT NULL,
										preference text NOT NULL);""")
	cursor.close()
	db.close()

setup_db()

def log_to_database(username,passwd,fname,age,rarestage,colorpreferred,posturepreferred,preference):
	db = sqlite3.connect("users.db")
	cursor = db.cursor()
	
	cursor.execute("""
				INSERT INTO users  (username,passwd,fname,age,rarestage,colorpreferred,posturepreferred,preference) 
				VALUES
				(?,?,?,?,?,?,?,?);""",
				(username,passwd,fname,age,rarestage,colorpreferred,posturepreferred,preference))
	db.commit()
	cursor.close()
	db.close()
 

def get_users():
	db = sqlite3.connect("users.db")
	cursor = db.cursor()
 
	res=cursor.execute("SELECT * FROM users")

	res = res.fetchall()

	cursor.close()
	db.close()
 
	return res
 
def get_user_password(username):
    results = get_users()
    passwd = None
    
    for user,passw,fname,age,rarestage,colorpreferred,posturepreferred,preference in results:
        if username.lower() == user.lower():
            passwd = passw
            break

    return passwd

def user_exists(username):
    res = get_user_password(username)
    if res:
        return True
    return False

def get_user(username,password):
    all_users = get_users()
    for user,passw,fname,age,rarestage,colorpreferred,posturepreferred,preference in all_users:
        if user.lower() == username.lower() and passw == password:
            return [user,passw,fname,age,rarestage,colorpreferred,posturepreferred,preference]
        
