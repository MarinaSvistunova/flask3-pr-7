import sqlite3
import math
import time

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getReviews(self):
        sql = '''SELECT * FROM reviews'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print("Couldn't read from database")
        return []

    def addReview(self, name, surename, email):
        try:
            self.__cur.execute("INSERT INTO registration VALUES(NULL, ?, ?, ?)", (name, surename, email))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Fall' + str(e))
            return False

        return True
    
    def addUser(self, name, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("You have been registered")
                return False
            
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?)", (name, email, hpsw, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Adding user faild' + str(e))
            return False
        
        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("There is not a such user")
                return False
            
            return res

        except sqlite3.Error as e:
            print('Serching user faild' + str(e))
        
        return False
    
    def getUserByEmail(self, email):
        try:
            print(email)
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("There is not a such user")
                return False
            
            return res

        except sqlite3.Error as e:
            print('Serching user faild' + str(e))
        
        return False
