import psycopg2

# This is my attemp at making an object-oriented approach at communicating with the database
# The goal is to make a user object, and link it to the database.

# Still a work in progress.

# connect to PostgreSQL database
connection = psycopg2.connect(
    dbname='NewDB',
    user='postgres',
    password='123456',
    host='localhost',
    port='5432'
)

class Student:
    
    username = ""
    password = ""
    major = ""

    def __init__(self, un, pswd, mjr):
        username = un
        password = pswd
        major = mjr
        
    def newEntry(self):
        cursor = connection.cursor()
        query = "INSERT INTO persons (username, password) VALUES (%s, %s, %s)"
        values = (self.username, self.password, self.major)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        print("Successful row insert")
        
    def searchEntry(self):
        cursor = connection.cursor()
        query = "SELECT EXISTS(SELECT 1 FROM persons WHERE name = %s)"
        match_val = self.username
        cursor.execute(query, (match_val,))
        result = cursor.fetchone()
        cursor.close()
        return result[0]
    
    def getUsername(self):
        exists = self.searchEntry(self.username)
        if exists:
            return self.username
        else:
            print("Username not in database")
            return
    
    def getPassword(self):
        exists = self.searchEntry(self.username)
        if exists:
            return self.password
        else:
            print("Password not in database")
            return
    
    def getMajor(self):
        exists = self.searchEntry(self.major)
        if exists:
            return self.major
        else:
            print("Major not in database")
            return

